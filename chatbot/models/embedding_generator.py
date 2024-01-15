import pinecone
import os
import re
import string
from langchain.vectorstores import Pinecone as VS
from tqdm.auto import tqdm  # for progress bar
import time
import pandas as pd
from bnlp import BasicTokenizer
from langchain.embeddings.openai import OpenAIEmbeddings
import PyPDF2

current_script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_script_dir)

class EmbeddingGenerator:
    def __init__(self, config):
        self.config = config
        self.pinecone_api_key = self.config["pinecone_api_key"]
        self.pinecone_index_name = self.config["pinecone_index_name"]
        self.openai_api_key = self.config["openai_key"]
        self.tokenizer =  BasicTokenizer()
        self.embeddings_model_name = self.config["embeddings_model_name"][0]
        #self.sentence_transformer = SentenceTransformer(self.embeddings_model_name)
        self.embed_model = OpenAIEmbeddings(model=self.embeddings_model_name, openai_api_key=self.openai_api_key)

        pinecone.init(api_key=self.pinecone_api_key, environment='gcp-starter')

        if self.pinecone_index_name not in pinecone.list_indexes():
            pinecone.create_index(self.pinecone_index_name, dimension=1536)  # Dimension depends on your model

        # Connect to the index
        self.index = pinecone.Index(self.pinecone_index_name)

    def load_data(self):
        # load text files from the data folder
        data = []
        for file in os.listdir(os.path.join(parent_dir, 'data')):
            filename = ''+os.path.join(parent_dir, 'data', file)
            filetype = file.split('.')[1] 
            if filetype not in self.config["supported_file_types"]:
                continue
            if filetype == 'pdf':
                print("pdf file found")
                with open(filename, 'rb') as file:
                    # Create a PDF reader object
                    reader = PyPDF2.PdfReader(file)
                    # Number of pages in the PDF
                    num_pages = len(reader.pages)

                    # Read each page
                    for page_num in range(num_pages):
                        page = reader.pages[page_num]
                        text = page.extract_text()
                        data.append(text)
            else:
                #load other files
                with open(filename, 'r') as f:
                    text = f.read()
                    data.append(text)
                    f.close()
        print("Data : ", len(data))
        return data
    

    def clean_and_preprocess_text(self,data):
        dataset = []
        for item in data:
            text = self.tokenizer(item)
            for i, chunk in enumerate(text):
                dataset.append({"chunk-id": i, "chunk": chunk})
            

        return dataset


    def create_embeddings(self):
        ''' Get the embeddings'''
        # check if embeddings already created
        stats = self.index.describe_index_stats()

        if stats['total_vector_count']>0:
            print("Embeddings already created")
            return VS(self.index, self.embed_model.embed_query, "text")
        
        # load data
        data = self.load_data()
        # clean and preprocess data
        data = self.clean_and_preprocess_text(data)
        data = pd.DataFrame(data)
        batch_size = 100

        for i in tqdm(range(0, len(data), batch_size)):
            i_end = min(len(data), i+batch_size)
            # get batch of data
            batch = data.iloc[i:i_end]
            # generate unique ids for each chunk
            ids = [f"{x['chunk-id']}" for i, x in batch.iterrows()]
            # get text to embed
            texts = [x['chunk'] for _, x in batch.iterrows()]
            # embed text
            embeds = self.embed_model.embed_documents(texts)
            time.sleep(60)
            # get metadata to store in Pinecone
            metadata = [
                {'text': x['chunk'],
            } for i, x in batch.iterrows()
            ]
            # add to Pinecone
            self.index.upsert(vectors=zip(ids, embeds, metadata))

        text_field = "text"  # the metadata field that contains our text

            # initialize the vector store object
        vectorstore = VS(self.index, self.embed_model.embed_query, text_field)

        print("Embeddings created successfully")
        return vectorstore

    def get_index_stats(self):
        ''' Get index stats'''
        return self.index.describe_index_stats()
