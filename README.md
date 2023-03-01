# TSI-Open-AI-Hackathon---Crisis-Avengers

![Solution Diagram](https://raw.githubusercontent.com/tferguson14/TSI-Open-AI-Hackathon---Crisis-Avengers/main/solution%20diagram.png)

# Background on Data - GDELT Project

[Gdelt Project](https://www.gdeltproject.org/)
GDELT 2.0 is a platform that monitors news reports breaking anywhere in the world, translates them in real-time, and processes them to identify events, sentiments, and themes, making this information available via an open metadata firehose for research purposes. It also focuses on non-Western media systems and incorporates sentiment mining through 24 emotional measurement packages.




## Code

### Hackathon Gdelt Article Text Data.py 

This python notebook pulls data Gdelt 2.0 events database and scrapes the text from the news events in preparation for Open AI summarization and classification.

### Getting results from Azure OpenAI and OpenAI

Suggested Prerequisites:
- Use [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)
- Use [miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Create a new conda python 3.8 environment. Don't use the base environment.

Prerequisites
- Python 3.8+
- Install the openai and langchain python libraries
- Obtain an [OpenAI]{https://openai.com/product) API key
- Or obtain an [Azure OpenAI]{https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview} API key

Steps
1. Setup environment variables for Python to use
  ``export OPENAI_API_KEY=``
Or if using Azure OpenAI
  ```export OPENAI_API_TYPE=azure
  export OPENAI_API_VERSION=2022-12-01
  export OPENAI_API_BASE=https://<your name>.openai.azure.com/
  export OPENAI_API_KEY=```
2. Run [tsi_hackathon.py}(https://github.com/tferguson14/TSI-Open-AI-Hackathon---Crisis-Avengers/blob/main/llm/code/tsi_hackathon.py)
