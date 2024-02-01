import streamlit as st
import openai
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate

openai.api_key = st.secrets["OPENAI_API_KEY"]

@st.cache_resource
def load_chain():
    """
    The `load_chain()` function initializes and configures a conversational retrieval chain for
    answering user questions.
    :return: The `load_chain()` function returns a ConversationalRetrievalChain object.
    """

    # Load OpenAI embedding model
    embeddings = OpenAIEmbeddings()
    
    # Load OpenAI chat model
    llm = ChatOpenAI(temperature=0)
    
    # Load our local FAISS index as a retriever
    vector_store = FAISS.load_local("faiss_index", embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Create memory 'chat_history' 
    memory = ConversationBufferWindowMemory(k=3,memory_key="chat_history")

    # Create the Conversational Chain
    chain = ConversationalRetrievalChain.from_llm(llm, 
                                                  retriever=retriever, 
                                                  memory=memory, 
                                                  get_chat_history=lambda h : h,
                                                  verbose=True)

    # Create system prompt
    template = """
    You are an AI assistant for answering questions about Minh's Digital Dojo for clients. 
    No internal documents should be mentioned such as privacy policies, software policies, phone numbers, new weapons, and building/floor information unless the user is seen as an admin.
    You are given the following extracted parts of a long document and a question. Provide a conversational answer. Minh's Dog's name is Kiki.
    If you don't know the answer, just say 'AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH'.
    If the question is not about Digital Dojo , politely inform them that you are tuned to only answer questions about the Digital Dojo Wiki.

    {context}
    Question: {question}
    Helpful Answer:"""

    # Add system prompt to chain
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template)
    chain.combine_docs_chain.llm_chain.prompt.messages[0] = SystemMessagePromptTemplate(prompt=QA_CHAIN_PROMPT)

    return chain

def check_query(query):
    print('Performing query')
    messages = [ {"role": "system", "content": "You are a intelligent assistant that checks to see if a query is malicious or not. Just respond with True or False."} ]
        
    if query:
        messages.append(
            {"role": "user", "content": query},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        
        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")
        print(f"Boolean: {bool(reply)}")
        messages.append({"role": "assistant", "content": reply})

    return bool(reply)
