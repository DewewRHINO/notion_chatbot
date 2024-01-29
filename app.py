import time
import streamlit as st
from utils import load_chain, check_query

# Custom image for the app icon and the assistant's avatar
company_logo = 'https://media.licdn.com/dms/image/D5603AQGArYlIrUfmHg/profile-displayphoto-shrink_200_200/0/1689743448626?e=1712188800&v=beta&t=2UzYe5l8cKMIhWt7uR21N41dYcjYgByTF80kxfVpwp0'

# Configure streamlit page
st.set_page_config(
    page_title="Minh's Digital Dojo ChatBot",
    page_icon=company_logo
)

# Initialize LLM chain in session_state
if 'chain' not in st.session_state:
    st.session_state['chain']= load_chain()

# Initialize chat history
if 'messages' not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "system", 
                                  "content": "Hello! I am Minh Tran's assistant, Minh Tran. I am here to answer any questions you may have about Minh or anything about his dojo."}]

# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=company_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat logic
if query := st.chat_input("Ask me anything"):
        
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant", avatar=company_logo):
        message_placeholder = st.empty()
        # Send user's question to our chain
        result = st.session_state['chain']({"question": query})
        response = result['answer']
        full_response = ""

        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})