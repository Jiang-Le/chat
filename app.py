import streamlit as st
import openai

def add_textbox(key, content):
    st.text_input(key, content)

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

prompt = st.text_input("Prompt")

if st.button('Send'):
    st.markdown('---')
    st.session_state.num_textboxes += 1
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",messages=st.session_state["messages"]
        )
        message_response = response["choices"][0]["message"]["content"]
        st.session_state.context.append({
            "user_prompt": prompt,
            "answer": message_response
        })

for i in range(st.session_state.num_textboxes):
    context = st.session_state.context[i]
    add_textbox(f"Question{i}", context["user_prompt"])
    add_text_area(f"Answer{i}", context["answer"])