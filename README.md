# Chat with RAG on Bangla Datasets
![Alt text](/ui.png)


## Overview

This repository hosts a web application built using Flask that enables users to interact with a large language model (LLM) in the Bengali language. The LLM is powered by OpenAI's text completion capabilities and leverages the RAG (Retrieve, Aggregate, Generate) methodology to provide informative answers to specific questions based on user-provided data in bangla language. The webapp uses an example document on bangladesh history for now. To add your own , you can follow the instructions below.

## Key Features

* Bengali language support: Specifically designed to handle Bengali text and datasets.
* OpenAI text completion: Utilizes OpenAI's powerful text completion API for generating responses.
* RAG methodology: Incorporates Retrieval, Aggregation, and Generation techniques for enhanced response quality.
* User-provided data: Allows users to supply their own data to train the LLM for question-answering tasks.
* Web interface: Offers a user-friendly web interface for interacting with the LLM.
* Bangla tokenizer:  [BNLP](https://github.com/sagorbrur/bnlp)
  
## Usage

Interact with the web app:

* Access the web application (link provided in the repository).
* Enter your questions in Bengali and receive responses from the LLM.
  
Implement your own data:

* Clone this repository.
* run ``` pip install -r requirements.txt ```
* Install python and OpenAI
* Add openai key to environment variable.
    * For example for macos run the command in the terminal. replace yourkey with your actual key:
       ```echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc  ```
    * next command to run:   ``` source ~/.zshrc ```
    * confirm by running this command in new terminal:   ``` echo $OPENAI_API_KEY ```
* put your datasets in the /data folder
* run the command: python call.py. this initializes the python script.

## Technical Details

* Framework: Flask
* Language model: OpenAI text completion
* Methodology: RAG (Retrieve, Aggregate, Generate)
* Language: Bengali

## Dependencies

Python 3.x
Flask
OpenAI API key
Other dependencies listed in requirements.txt

