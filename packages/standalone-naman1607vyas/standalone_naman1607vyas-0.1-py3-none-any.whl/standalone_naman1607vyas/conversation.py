import openai
from .retriever import retrieve_context

def generate_standalone_question(memory):
    chat_history = memory.load_memory_variables({}).get("chat_history", "")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Create standalone questions."},
            {"role": "user", "content": f"Chat history:\n{chat_history}"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()


def chat_with_memory(query, memory, embedding_model, faiss_index, documents):
    # Create the OpenAI Chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Replace with your desired model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )

    # Extract the response content as a string
    assistant_response = response["choices"][0]["message"]["content"]

    # Save context to memory
    memory.save_context({"User": query}, {"Assistant": assistant_response})

    return assistant_response

