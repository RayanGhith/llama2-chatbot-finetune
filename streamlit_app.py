import streamlit as st
from transformers import pipeline

# App title
st.set_page_config(page_title="Chatbot with Hugging Face Model")

# Model selection from Hugging Face Hub
with st.sidebar:
    st.title('Chatbot with Hugging Face Model')
    model_name = st.selectbox('Choose a model:', ['oumaima12/Llama-2-7b-chat-finetune6'], key='selected_model')
    loaded_model = pipeline(task="conversational", model=model_name)  # Adjust task as needed
    st.subheader('Conversation Parameters')
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)

# Store conversation history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating response
def generate_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    response = loaded_model(inputs=prompt_input, max_length=max_length, num_beams=1, temperature=temperature, top_p=top_p)[0]['generated_text']
    return response

# User-provided prompt
if prompt := st.chat_input(placeholder="Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
