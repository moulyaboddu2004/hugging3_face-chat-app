import streamlit as st
import requests

st.title("🤖 Hugging Face Chat Assistant")

# Input field
user_input = st.text_input("You:")

if user_input:
    st.info("⏳ Sending your message... Please wait.")

    # Use a different model (google/flan-t5-base)
    API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
    headers = {"Authorization": f"Bearer {st.secrets['hf_token']}"}
    prompt = f"Answer this politely like a chatbot: {user_input}"
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        try:
            generated_text = data[0]["generated_text"]
            st.success("🤖 Assistant:")
            st.write(generated_text)
        except Exception as parse_err:
            st.error("❌ Couldn't extract text from the response.")
            st.write("Raw API response:")
            st.json(data)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error: {http_err}")
        st.text(response.text)
    except Exception as e:
        st.error("❌ Something else went wrong:")
        st.exception(e)

