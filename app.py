import streamlit as st
import requests

st.title("🤖 Hugging Face Chat Assistant")

user_input = st.text_input("You:")

if user_input:
    st.info("⏳ Sending your message... Please wait...")

    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {
        "Authorization": f"Bearer {st.secrets['hf_token']}"
    }

    prompt = f"{user_input}"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        try:
            answer = data[0]["generated_text"]
            st.success("🤖 Assistant:")
            st.write(answer.strip())
        except Exception:
            st.error("❌ Couldn't parse the model response.")
            st.write("Full response:")
            st.json(data)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error: {http_err}")
        st.text(response.text)
    except Exception as e:
        st.error("❌ Something went wrong:")
        st.exception(e)





