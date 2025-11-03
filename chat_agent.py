from google import genai
import streamlit as st


st.title("Chat Agent")

api_key = st.sidebar.text_input("Enter your API Key")
st.sidebar.button("Submit")

model = "gemini-2.5-flash"
content = "Which model is used to generate the response?"

if not api_key:
    st.info("Please enter your API key")
else:
    # Initialize Google API client
    try:
        client = genai.Client(api_key=api_key)
        # Below first call will also validate the API key is valid
        response = client.models.generate_content(model=model, contents=content)

    except Exception as e:
        with st.chat_message("assistant"):
            st.markdown(e.message)
        st.stop()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Hello. How can I help you?")
    if prompt:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = client.models.generate_content(model=model, contents=prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response.text)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )
