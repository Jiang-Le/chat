import streamlit as st
import openai

def format_user_prompt(text):
    return f'<p style="background-color:#F0F2F6;padding: 8px;border-radius: 5px"><span style="font-weight:bold">Question</span>: {text}</p>'

def add_textbox(key, content):
    st.markdown(content, unsafe_allow_html=True)

def add_text_area(key, content):
    st.markdown(content)

if 'num_textboxes' not in st.session_state:
    st.session_state.num_textboxes = 0

if 'context' not in st.session_state:
    st.session_state.context = []

BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

openai.api_key = st.text_input("Paste your OpenAI API Key here", value="", type="password")

for i in range(st.session_state.num_textboxes):
    context = st.session_state.context[i]
    add_textbox(f"Question{i}", format_user_prompt(context["user_prompt"]))
    add_text_area(f"Answer{i}", context["answer"])

place_holder = st.empty()
place_holder2 = st.empty()

prompt = st.text_input("Prompt")

if st.button('Send'):
    st.markdown('---')
    with st.spinner("Generating response..."):
        messages = st.session_state["messages"]
        messages += [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",messages=messages
        )
        message_response = response["choices"][0]["message"]["content"]
        st.session_state.context.append({
            "user_prompt": prompt,
            "answer": message_response
        })
        st.session_state["messages"] = messages
        
        st.session_state.num_textboxes += 1
        place_holder.markdown(format_user_prompt(prompt), unsafe_allow_html=True)
        place_holder2.markdown(message_response)
