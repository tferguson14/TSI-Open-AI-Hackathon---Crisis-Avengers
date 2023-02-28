# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC #Download Events Data from Gdelt Site

# COMMAND ----------

import os
import pandas as pd
import urllib
import re
import zipfile

# Global variables/search parameters
start_date = '2023-02-01'
end_date = '2023-02-02'
main_dir = '/dbfs/user'
output_dir = '/dbfs/user'
output_file = 'eventsdata_sample.csv'

# Define search range
def get_date_time_intervals(start_date, end_date):
    date_time_range = pd.date_range(start=start_date, end=end_date, freq='15T')
    return [str(date) for date in date_time_range]

date_range = get_date_time_intervals(start_date, end_date)
date_range = date_range[:30]

# Download and extract the GKG data
batch_size_date = 100
num_batches_date = (len(date_range) + batch_size_date - 1) // batch_size_date

gkg2_cols = ['GKGRECORDID', 'DATE', 'SourceCollectionIdentifier', 'SourceCommonName',
             'DocumentIdentifier', 'Counts', 'V2Counts', 'Themes', 'V2Themes',
             'Locations', 'V2Locations', 'Persons', 'V2Persons', 'Organizations',
             'V2Organizations', 'V2Tone', 'Dates', 'GCAM', 'SharingImage',
             'RelatedImages', 'SocialImageEmbeds', 'SocialVideoEmbeds', 'Quotations',
             'AllNames', 'Amounts', 'TranslationInfo', 'Extras']

gkg2_batches = []
for batch in range(num_batches_date):
    print('Batch:', batch)
    # Instantiate df for batch of news
    gkg2 = pd.DataFrame(columns=gkg2_cols)

    for count, date in enumerate(date_range[batch*batch_size_date:(batch+1)*batch_size_date]):
        if count % 48 == 0:
            print(date)
        date_str = re.sub(r'[^\d+]', '', date)
        url = f'http://data.gdeltproject.org/gdeltv2/{date_str}.gkg.csv.zip'

        try:
            # Fetch GKG data
            with urllib.request.urlopen(url) as resp:
                data = resp.read()
            # Write to file
            with open(os.path.join(main_dir, f"{date_str}.gkg.csv.zip"), "wb") as f:
                f.write(data)
            # Unzip compressed file and extract contents
            with zipfile.ZipFile(os.path.join(main_dir, f'{date_str}.gkg.csv.zip'), 'r') as zip_ref:
                zip_ref.extractall(main_dir)
            # Read news contents from date
            df = pd.read_csv(os.path.join(main_dir, f'{date_str}.gkg.csv'), lineterminator='\n',
                             delimiter='\t', encoding='latin1', header=None, names=gkg2_cols)
            # Append day's news to df for batch
            gkg2 = pd.concat([gkg2, df], ignore_index=True)
        except Exception as e:
            print(f"Failed to download {url}: {e}")

        # Remove zip and individual files
        os.remove(os.path.join(main_dir, f'{date_str}.gkg.csv.zip'))
        os.remove(os.path.join(main_dir, f'{date_str}.gkg.csv'))

    # To datetime object
    gkg2.DATE = pd.to_datetime(gkg2.DATE, format='%Y%m%d%H%M%S')
   
print('Original Shape:', gkg2.shape)
gkg2 = gkg2.dropna(subset=['Locations', 'Themes'])
print('DropNA:', gkg2.shape)
sample_df = gkg2.sample(n=100, random_state=42)
print('sample:', sample_df.shape)
sample_df.to_csv(os.path.join(output_dir,output_file))

display(sample_df)

# COMMAND ----------

!pip install newspaper3k

# COMMAND ----------

# MAGIC %md
# MAGIC #Scrape Text from Websites

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import newspaper
from urllib.error import HTTPError

main_dir = '/dbfs/user'
output_dir = '/dbfs/user'
output_file = 'eventsdata_sample_text.csv'

# Define a function to extract main text content from a URL using newspaper3k
def extract_text(url):
    article = newspaper.Article(url)
    try:
        article.download()
        article.parse()
        return article.text if article.text else None
    except HTTPError as e:
        if e.code == 403:
            print(f"Access denied: {url}")
            return None
        else:
            raise e
    except:
        print(f"Error processing URL: {url}")
        return None

# Create a SparkSession
spark = SparkSession.builder.appName("ExtractTextFromUrls").getOrCreate()

# Load the CSV file as a DataFrame
df = spark.read.csv("dbfs:/user/eventsdata_sample.csv", header=True, inferSchema=True)

# Define a UDF to apply the extract_text function to each URL in the DataFrame
extract_text_udf = udf(extract_text, StringType())

# Add a new column to the DataFrame that contains the extracted text from each URL
df = df.withColumn("Text", extract_text_udf(df["DocumentIdentifier"]))

# Export the resulting DataFrame to a new CSV file
#df.write.csv(os.path.join(output_dir,output_file))

df.write.mode("overwrite").csv("dbfs:/user/eventsdata_sample_text.csv")

display(df)

# COMMAND ----------


