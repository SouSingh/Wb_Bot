import openai
from dotenv import load_dotenv
import os
import json
import streamlit as st
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleFileNodeParser
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
import weaviate
from llama_index.llms.clarifai import Clarifai

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')
os.environ["CLARIFAI_PAT"] = os.getenv("CLARIFAI_PAT")
openai.api_key = api_key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
auth_config = weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)

client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=auth_config
)

def query_weaviate(ask):
    vector_store = WeaviateVectorStore(weaviate_client=client, index_name="NABSH")
    loaded_index = VectorStoreIndex.from_vector_store(vector_store)
    query_engine = loaded_index.as_query_engine(include_text=True,
                                                response_mode="tree_summarize",
                                                embedding_mode="hybrid",
                                                similarity_top_k=5,)
    message_template = f"""<|system|>Please check if the following pieces of context has any 
    mention of the keywords provided in the Question and please try to give correct answer 
    if user ask simple answer then give simple answer otherwise he asked summary then give '
    summary and produce accurate and clean source node which is readable from starting to end</s>
    <|user|>
    Question: {ask}
    Helpful Answer:
    </s>"""
    print("Done 2")
    response = query_engine.query(message_template)
    print("Done 4")
    return response


def contract_analysis_w_fact_checking(text):
    if not text:
        st.error("Text field is required in the input data.")
        return

    # Perform contract analysis using query_weaviate (assuming it's a function)
    quert_instance = query_weaviate(text)
    llmresponse = quert_instance.response
    #node 1
    nodes = []
    for nexted in quert_instance.source_nodes:
        dat = nexted.node.text
        nodes.append(dat)


    return llmresponse, nodes

def convert_to_readable(text_list):
    llm_model = Clarifai(model_url="https://clarifai.com/openai/chat-completion/models/gpt-4-turbo")
    summary = llm_model.complete(prompt=f'''
            Please generate a concise summary of the following text into points so that user can understand easily if points neccesary generate points otherwise give simple text in summary so that user understand easily

            Transcription: {text_list}
            ''')
    summary = (str(summary))
    
    return summary

def main():
    st.title("Easework chat")

    user_message = st.text_input("Enter your text:")
    if st.button("Analyze"):
        llmresponse, nodes = contract_analysis_w_fact_checking(user_message)
        readable_text = convert_to_readable(nodes)
        st.write(f"LLM Response: {llmresponse}")
        st.subheader("Realtive Answer from book")
        st.write(f"Text: {readable_text}")

if __name__ == "__main__":
    main()