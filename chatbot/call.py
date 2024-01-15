import time
from config import get_configurataion
from models.llm import LLModel
from models.embedding_generator import EmbeddingGenerator

def launchbot(configs):
    
    pinecone = EmbeddingGenerator(configs)
    # create embeddings
    vectorstore  = pinecone.create_embeddings()
    print(pinecone.get_index_stats())

    AI = LLModel(configs, vectorstore)

    return AI
       

if __name__ == "__main__":

    configs = get_configurataion()
    AI = launchbot(configs)

    while True:
        question = input("এখানে আপনার প্রশ্ন লিখুন: ")
        if question == "exit":
            break
        start_time = time.time()
        response = AI.get_response(question)


        print("\n Time taken: ", round(time.time() - start_time,3), 'sec  \n')
        print("\033[92m" + response + "\033[0m")



