import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate

# 🔹 Add your API Key here
API_KEY = "your_api_key_here"

# Initialize the AI model
llm = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=API_KEY)

# Initialize session state for memory persistence
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)  # 🔹 Memory persists

# Define conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=st.session_state.memory,  # 🔹 Uses persistent session memory
    prompt=PromptTemplate(
        input_variables=["history", "input"],
        template="You are a data science tutor. Answer only data science-related questions. Keep the conversation natural and informative. \n\n{history}\nUser: {input}\nTutor:"
    )
)

# Set up Streamlit UI
st.title("🤖 Conversational AI Data Science Tutor")
st.write("Ask me any Data Science questions!")

# Input box for user query
user_input = st.text_input("Your Question:", "")

if user_input:
    response = conversation.run(user_input)
    st.write("**Tutor:**", response)

# 🔍 Display **full** stored conversation history
st.write("### 🔄 Conversation History:")
messages = st.session_state.memory.chat_memory.messages  # Correctly retrieves history

if messages:
    for msg in messages:
        role = "👤 User:" if msg.type == "human" else "🤖 Tutor:"
        st.write(f"{role} {msg.content}")
else:
    st.write("No conversation history yet.")
