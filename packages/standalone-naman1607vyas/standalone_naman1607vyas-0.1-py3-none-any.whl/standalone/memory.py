from langchain.memory import ConversationBufferMemory

def get_conversation_memory(max_size=5):
    return ConversationBufferMemory(memory_key="chat_history", max_size=max_size)
