from standalone.config import API_KEY
from standalone.memory import get_conversation_memory
from standalone.retriever import initialize_retriever
from standalone.conversation import chat_with_memory
from datasets import load_dataset
import openai

openai.api_key = API_KEY

if __name__ == "__main__":
    ds = load_dataset("LangChainDatasets/question-answering-state-of-the-union")
    documents = [item["answer"] for item in ds["train"]]
    
    faiss_index, embedding_model = initialize_retriever(documents)
    memory = get_conversation_memory()

    while True:
        query = input("Your Query: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = chat_with_memory(query, memory, embedding_model, faiss_index, documents)
        print("\nAssistant Response:", response)
