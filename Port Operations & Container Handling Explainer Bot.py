import streamlit as st
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyApuy8TeUHabFzS7XOWI6Zw7P_LXTGhddk")
MODEL_NAME = "gemini-3-flash-preview"

SYSTEM_PROMPT = """
You are a domain-restricted AI assistant dedicated only to explaining
port operations, container handling, vessel arrival, yard operations,
and maritime logistics workflows.

You must politely refuse to answer any query outside Ports & Shipping.
You must not perform or suggest operational decisions such as vessel
scheduling, cargo approval, or container movement.
Your responses are for training and awareness only.
"""

st.set_page_config(page_title="Port Operations Explainer Bot", layout="centered")
st.title("🚢 Port Operations & Container Handling Explainer Bot")
st.caption("Informational AI for Ports & Maritime Logistics Training")


user_input = st.text_area(
    "Ask a question about port operations or container handling:",
    placeholder="e.g., Explain container handling process",
    height=120
)


if st.button("Explain"):
    if not user_input.strip():
        st.warning("Please enter a port-related question.")
    else:
        with st.spinner("Generating explanation..."):
            try:
                # Prepare contents with system + user message
                contents = [
                    types.Content(
                        role="system",
                        parts=[types.Part.from_text(text=SYSTEM_PROMPT)]
                    ),
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=user_input)]
                    )
                ]

                # Generate Content Config
                config = types.GenerateContentConfig(
                    temperature=0.25,
                    thinking_config=types.ThinkingConfig(thinking_level="HIGH")
                )

                # Call Gemini Flash Model
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents,
                    config=config
                )

                st.markdown("### 📘 Explanation")
                st.write(response.text)

            except Exception as e:
                st.error(f"Error generating response: {e}")
