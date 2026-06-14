import streamlit as st
from openai import OpenAI


# =========================
# 1. Basic page settings
# =========================
st.set_page_config(
    page_title="Kyrie's AI Portfolio Assistant",
    page_icon="🤖",
    layout="centered"
)


# =========================
# 2. Connect to OpenAI API
# =========================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# =========================
# 3. Read your profile information
# =========================
with open("profile.md", "r", encoding="utf-8") as file:
    profile_info = file.read()


# =========================
# 4. Define the chatbot's behavior
# =========================
system_prompt = f"""
You are Kyrie (Wentao) Jiang's professional AI portfolio assistant.

Your job:
- Help recruiters, classmates, and collaborators understand Kyrie's background.
- Answer questions about Kyrie's education, technical skills, projects, and career interests.
- Use a professional, friendly, and concise tone.

Important rules:
- Use only the information provided in the profile below.
- Do not invent experiences, companies, awards, grades, job titles, or technical skills.
- If the answer is not included in the profile, say: "I don't have enough information about that from Kyrie's profile."
- If someone wants to contact Kyrie, suggest contacting Kyrie through LinkedIn.

Profile information:
{profile_info}
"""


# =========================
# 5. Page title and introduction
# =========================
st.title("🤖 Kyrie's AI Portfolio Assistant")

st.write(
    "Ask me about Kyrie's projects, technical skills, education, "
    "and career interests."
)

st.caption(
    "This chatbot is based on Kyrie's self-provided profile information."
)


# =========================
# 6. Initialize chat history
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# 7. Display previous chat messages
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# 8. Get user input
# =========================
user_input = st.chat_input("Ask about my projects, skills, or experience...")


# =========================
# 9. Generate assistant response
# =========================
if user_input:
    # Save user's message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Display user's message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare messages for the model
    api_input = [
        {"role": "developer", "content": system_prompt},
        *st.session_state.messages
    ]

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.responses.create(
                model="gpt-5.4-nano",
                input=api_input,
                max_output_tokens=600
            )

            answer = response.output_text
            st.markdown(answer)

    # Save assistant's response
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )