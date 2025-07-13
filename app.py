import streamlit as st
import requests

st.title("🤖 Hugging Face Chat Assistant")

user_input = st.text_input("You:")

if user_input:
    st.info("⏳ Sending your message... Please wait...")

    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {
        "Authorization": f"Bearer {st.secrets['hf_token']}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": f"<s>[INST] {user_input} [/INST]",
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.7,
            "do_sample": True
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        try:
            generated_text = data[0]["generated_text"]
            assistant_reply = generated_text.split("[/INST]")[-1].strip()
            st.success("🤖 Assistant:")
            st.write(assistant_reply)
        except Exception as parse_err:
            st.error("❌ Couldn't parse the model response.")
            st.json(data)

    except requests.exceptions.HTTPError as http_err:
        st.error(f"❌ HTTP error: {http_err}")
        st.text(response.text)
    except Exception as e:
        st.error("❌ Something went wrong:")
        st.exception(e)



