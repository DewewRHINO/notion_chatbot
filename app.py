import time
import streamlit as st
from utils import load_chain  # Assuming this is where your chat logic and loading functions are defined

# Custom image for the app icon and the assistant's avatar
company_logo = 'https://media.licdn.com/dms/image/D5603AQGArYlIrUfmHg/profile-displayphoto-shrink_200_200/0/1689743448626?e=1712188800&v=beta&t=2UzYe5l8cKMIhWt7uR21N41dYcjYgByTF80kxfVpwp0'

gif_url = "https://cdn.discordapp.com/attachments/973058108114997269/1203110648712536124/minhdissapearing.gif?ex=65cfe71b&is=65bd721b&hm=4a67d4092c4a258fd476783ad910ec3edbc2f971b852ae36066f87eba7f3dbdb&"  # Example GIF URL

# Configure streamlit page
st.set_page_config(
    page_title="Minh's Digital Dojo ChatBot",
    page_icon=company_logo
)

# Initialize LLM chain in session_state if not already initialized
if 'chain' not in st.session_state:
    st.session_state['chain'] = load_chain()

# Initialize chat history if not already initialized
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "system", 
                                     "content": "Hello! I am Minh Tran's assistant, Minh Tran. I am here to answer any questions you may have about Minh or anything about his dojo."}]

# Display chat messages from history on app rerun
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
        
    # Check for specific keywords in the query
    sensitive_keywords = ["admin", "phone number", "password", "minh"]
    if any(keyword in query.lower() for keyword in sensitive_keywords):
        # Display the GIF without sending the query to the chain
        with st.chat_message("assistant", avatar=company_logo):
            st.image(gif_url, caption="Oops, let's not talk about that here!")
            
        # Add a generic assistant message to chat history to maintain flow
        st.session_state.messages.append({"role": "assistant", "content": "Oops, let's not talk about that here!"})
    else:
        # Process query normally if no sensitive keywords are found
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
