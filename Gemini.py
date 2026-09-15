import json
import requests
import streamlit as st


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Gemini Chat",
    page_icon="✦",
    layout="wide"
)


# -----------------------------
# Gemini Configuration
# -----------------------------
API_KEY = 'AIzaSyAfDPUtNXsNRjq1JHDkUdlGnVZoHK4nJX8'

MODEL = "gemini-3.1-flash-lite"

URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{MODEL}:streamGenerateContent"
    f"?alt=sse&key={API_KEY}"
)


# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("✦ Gemini Chat")

    st.caption("Powered by Google Gemini")

    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.write("**Model**")
    st.code(MODEL)

    st.divider()

    st.caption("Gemini API • Streamlit • requests")


# -----------------------------
# Main UI
# -----------------------------
st.title("How can I help you?")

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show token information if available
        if message["role"] == "assistant" and "usage" in message:
            usage = message["usage"]

            with st.expander("Token usage"):
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Input tokens",
                    usage.get("promptTokenCount", 0)
                )

                col2.metric(
                    "Output tokens",
                    usage.get("candidatesTokenCount", 0)
                )

                col3.metric(
                    "Total tokens",
                    usage.get("totalTokenCount", 0)
                )


# -----------------------------
# Gemini Streaming Function
# -----------------------------
def stream_gemini(messages):

    contents = []

    for message in messages:

        contents.append({
            "role": (
                "user"
                if message["role"] == "user"
                else "model"
            ),
            "parts": [
                {
                    "text": message["content"]
                }
            ]
        })

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    try:

        response = requests.post(
            URL,
            json=payload,
            stream=True,
            timeout=120
        )

        if response.status_code != 200:

            try:
                error = response.json()
                error_message = error.get(
                    "error",
                    {}
                ).get(
                    "message",
                    "Unknown Gemini API error"
                )
            except Exception:
                error_message = response.text

            yield f"API Error: {error_message}"
            return

        for line in response.iter_lines():

            if not line:
                continue

            # SSE format:
            # data: {...}
            if line.startswith(b"data: "):

                data = line[6:].decode("utf-8")

                try:

                    chunk = json.loads(data)

                    # -------------------------
                    # Extract text
                    # -------------------------
                    candidates = chunk.get(
                        "candidates",
                        []
                    )

                    if candidates:

                        parts = candidates[0].get(
                            "content",
                            {}
                        ).get(
                            "parts",
                            []
                        )

                        for part in parts:

                            text = part.get("text")

                            if text:
                                yield text

                    # -------------------------
                    # Extract usage metadata
                    # -------------------------
                    usage = chunk.get(
                        "usageMetadata"
                    )

                    if usage:
                        st.session_state["latest_usage"] = usage

                except json.JSONDecodeError:
                    continue

    except requests.exceptions.Timeout:

        yield "Request timed out. Please try again."

    except requests.exceptions.RequestException as e:

        yield f"Request failed: {e}"


# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Message Gemini...")


if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare response
    with st.chat_message("assistant"):

        # Reset token information
        st.session_state["latest_usage"] = {}

        # Stream response
        response_text = st.write_stream(
            stream_gemini(
                st.session_state.messages
            )
        )

        # Make sure response is a string
        if not isinstance(response_text, str):
            response_text = "".join(response_text)

        # Get usage information
        usage = st.session_state.get(
            "latest_usage",
            {}
        )

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "usage": usage
        })

        # -------------------------
        # Token Display
        # -------------------------
        if usage:

            with st.expander("Token usage"):

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Input tokens",
                    usage.get(
                        "promptTokenCount",
                        0
                    )
                )

                col2.metric(
                    "Output tokens",
                    usage.get(
                        "candidatesTokenCount",
                        0
                    )
                )

                col3.metric(
                    "Total tokens",
                    usage.get(
                        "totalTokenCount",
                        0
                    )
                )