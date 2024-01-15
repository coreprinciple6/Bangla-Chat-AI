import os

def get_configurataion():
    ''' Get the configuration of the project'''
    config = {
        "Bot_persona": ["You are a helpful assistant with in-depth knowledge in bangla language. please answer all questions in bangla and make sure that the answers are grammatically correct.do not make up information. understand the context carefully. Look for answers in the knowledge base."],
        "openai_model_name": ["gpt-4-1106-preview"],
        "openai_key": os.environ["MY_OPENAI_API_KEY"],
        "embeddings_model_name": ["text-embedding-ada-002"],
        "pinecone_api_key": os.environ["MY_PINECONE_API_KEY"],
        "pinecone_index_name": "bangla-ai",
        "Knowledge_base": ["data"],
        "supported_file_types": ['c', 'cpp', 'csv', 'docx', 'html', 'java', 'json', 'md', 'pdf', 'php', 'pptx', 'py', 'rb', 'tex', 'txt', 'css', 'jpeg', 'jpg', 'js', 'gif', 'png', 'tar', 'ts', 'xlsx', 'xml', 'zip'],
        
    }

    return config