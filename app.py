import streamlit as st
import requests

st.title("🤖 Hugging Face Chat Assistant")

# Input field
user_input = st.text_input("You:")

if user_input:
    st.info("⏳ Sending your message... Please wait.")

    # Hugging Face API URL
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}
    payload = {"inputs": {"text": user_input}}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Will raise error for 4xx or 5xx

        data = response.json()
        st.success("🤖 Assistant:")

        # Safely extract generated text
        try:
            generated_text = data[0]["generated_text"]
            st.write(generated_text)
        except Exception as parse_err:
            st.error("❌ Couldn't extract response from the model.")
            st.write("Raw API Response:")
            st.json(data)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error: {http_err}")
        st.text(response.text)

    except Exception as e:
        st.error("❌ Something else went wrong:")
        st.exception(e)
