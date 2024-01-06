import streamlit as st
from streamlit_chat import message
import json

# vertex ai
from google.oauth2 import service_account
import vertexai

# utils
from utils.get_pdf import get_pdf_text
from utils.get_chunk import get_text_chunks
from utils.conversation_chain import conversation_chain
from utils.get_embedding import get_vector_store

st.set_page_config(page_title = "Chat with Multiple PDFs", page_icon = ":books")


with st.sidebar:
    # upload a PDF file
    pdf_docs = st.file_uploader("Upload your PDFs", type='pdf', key="pdf_docs", accept_multiple_files=True)
    key = st.file_uploader("Upload your GCP Service Account", type='json', key="key")
    project = st.text_input("Project ID", type="password")

    submit = st.button("Save")

    # session states
    if "file" not in st.session_state:
        st.session_state["file"] = pdf_docs

    if "json" not in st.session_state:
        st.session_state["json"] = key
    
    if "project_id" not in st.session_state:
        st.session_state["project_id"] = project

    # save button
    if submit:
        if pdf_docs is not None:
            st.session_state["file"] = pdf_docs
        if key is not None and project is not None:
            st.session_state["json"] = key
            st.session_state['project_id'] = project
            file_content = st.session_state['json'].getvalue()
            json_content = json.loads(file_content)
            credentials = service_account.Credentials.from_service_account_info(json_content)
            vertexai.init(project=st.session_state['project_id'], credentials=credentials)

        with st.spinner("Processing"):
            raw_text = get_pdf_text(pdf_docs)
            
            text_chunks = get_text_chunks(raw_text)
            
            vector_store = get_vector_store(text_chunks)

            if "vectorstore" not in st.session_state:
                st.session_state["vectorstore"] = vector_store
            
            

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []


prompt = st.text_input("Prompt", placeholder="Enter your question here...") or st.button(
    "Submit"
)

if prompt:
    with st.spinner("Generating response..."):
        generated_response = conversation_chain(
            st.session_state["vectorstore"], query=prompt, chat_history=st.session_state["chat_history"]
        )

        
        formatted_response = (
            f"{generated_response['answer']}"
        )

        st.session_state.chat_history.append((prompt, generated_response["answer"]))
        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answers_history.append(formatted_response)

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(
            user_query,
            is_user=True,
            key=hash(user_query)
        )
        message(generated_response)