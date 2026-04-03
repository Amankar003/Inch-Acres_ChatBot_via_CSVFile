import streamlit as st 
from backend import load_csv, create_agent, ask_question

st.set_page_config(page_title="Inch&Acre AI Consultant", layout="wide")
st.title("🏡 Inch&Acre Real Estate Chatbot")

# Session states initialize karo
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "agent" not in st.session_state:
    st.session_state.agent = None

with st.sidebar:
    uploaded_file = st.file_uploader("Upload Property Data (CSV or Excel)", type=["csv"])
    if st.button("Reset Chat"):
        st.session_state.chat_history = []
        st.rerun()

if uploaded_file:
    if "df" not in st.session_state:
        st.session_state.df = load_csv(uploaded_file)
        st.session_state.agent = create_agent(st.session_state.df)

    # Chat history display karo
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Type your message here..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("Aman is thinking..."):
                history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.chat_history[-5:]])
                answer = ask_question(st.session_state.agent, prompt, history_str)
                st.markdown(answer)
        
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

else:
    st.info("First upload the file for continue.....")