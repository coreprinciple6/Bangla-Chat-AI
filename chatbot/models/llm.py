from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class LLModel():
    def __init__(self, config, vectorstore):
        self.config = config
        self.llmmodel = ChatOpenAI(temperature=0, openai_api_key=self.config['openai_key'], model=self.config['openai_model_name'][0] )
        self.vectorstore = vectorstore

    def get_response(self, query):


        retriever, retrieved_docs = self.retrieve_docs(query)
        persona = ""+self.config['Bot_persona'][0]
        template = persona + """ Use the following pieces of retrieved context in bangla to answer the question in bangla.
              Context:{context}
              Question: {question}"""
        rag_prompt_custom = PromptTemplate.from_template(template)

        rag_chain = ( 
            {"context": retriever | self.format_docs , "question": RunnablePassthrough()}
            | rag_prompt_custom 
            | self.llmmodel  
            | StrOutputParser() )

        response = rag_chain.invoke(query)
            
        return response

    def format_docs(self,docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def retrieve_docs(self,query):
        ''' Search embeddings'''
        retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
        retrieved_docs = retriever.get_relevant_documents(query)

        return retriever,retrieved_docs
    
