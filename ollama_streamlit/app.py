import streamlit as st
from ollama import Client

#connect to local Ollama
ollama_client = Client(host='http://localhost:11434/')
print(f'ollama client connection : {ollama_client}')

st.title("Ollama Local AI Chatbot (Streamlit + Ollama)")

#chat history
if not st.session_state:
    st.session_state.messages = []


#show chathistroy
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])
        
#user input
prompt = st.chat_input("Ask me anything ...")
if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content" : prompt
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
        
    #Model response
    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ''
        
        stream = ollama_client.chat(
            model="llama3",
            messages=st.session_state.messages,
            stream=True
        )
        
        for chunk in stream:
            token = chunk["message"]["content"]
            full_response += token
            response_placeholder.markdown(full_response)
        
        
        st.session_state.messages.append(
            {
                'role': "assistant",
                'content' : full_response
            }
        )
        
