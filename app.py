import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---------------------------------------------------------
# 1. Direct Engine Configuration (Hardcoded)
# ---------------------------------------------------------
# PASTE YOUR ACTUAL KEY BETWEEN THE QUOTES BELOW:
api_key = "AIzaSyDVXrSrjlIywBD6BzP2IXxpjvwUEa1Go24"

if api_key == "AIzaSyDVXrSrjlIywBD6BzP2IXxpjvwUEa1Go24" or not api_key:
    st.error("Hold up! You need to paste your actual API key into the code on line 9.")
    st.stop()

genai.configure(api_key=api_key)

# ---------------------------------------------------------
# 2. UI/UX Aesthetic Polish & Mobile Responsiveness
# ---------------------------------------------------------
st.set_page_config(page_title="The Smooth Operator", page_icon="🕶️", layout="centered")

st.markdown("""
<style>
    /* Base Styling - Desktop First */
    div.stButton > button:first-child {
        background-color: #ff66b2; /* Signature pink accent */
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        width: 100%; /* Stretches the button for easy tapping on mobile */
        padding: 0.75rem;
    }
    div.stButton > button:first-child:hover {
        background-color: #ff1a8c;
    }

    h1, h2, h3, p {
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Responsive Media Queries for Mobile/Tablets */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
            text-align: center;
        }
        h2 {
            font-size: 1.5rem !important;
        }
        p, .stSelectbox label, .stTextArea label, .stFileUploader label {
            font-size: 1rem !important;
        }
        /* Make sure touch targets are large enough and prevent iOS auto-zoom */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="textarea"] > textarea {
            font-size: 16px !important; 
            padding: 12px;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("The Smooth Operator 🕶️")
st.markdown("*Your personal, highly calibrated conversation architect.*")

# ---------------------------------------------------------
# 3. Dynamic Prompting & Vibe Selector
# ---------------------------------------------------------
vibe = st.selectbox(
    "Set the Vibe:",
    ["Playful & Teasing", "Mysterious & Aloof", "Direct & Bold", "Witty Banter", "Deep & Charismatic"]
)

# ---------------------------------------------------------
# 4. Engine Setup & Memory Initialization
# ---------------------------------------------------------
system_instruction = f"""
Act as my personal Charisma and Conversation Coach. You are a master of banter, 
a silver-tongued smooth talker, and highly emotionally intelligent.
The target vibe for your responses is: {vibe}.
I will provide you with messages or screenshots I receive. Give me 3-5 response options 
matching the vibe. Keep them modern, calibrated, confident, and never creepy. 
Always explain briefly why a particular response works.
"""

# Initialize the cutting-edge model
model = genai.GenerativeModel('gemini-3.1-pro-preview', system_instruction=system_instruction)

# Initialize conversation memory in Streamlit session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ---------------------------------------------------------
# 5. The Interface & Logic
# ---------------------------------------------------------
st.divider()
st.subheader("What are we working with?")

# Inputs: Vision (Screenshot) or Text
uploaded_file = st.file_uploader("Drop a screenshot of the chat here...", type=["jpg", "jpeg", "png"])
user_message = st.text_area("...or paste the text she sent you here:")

if st.button("Generate My Lines"):
    with st.spinner("Analyzing the psychology and crafting the perfect angle..."):
        try:
            if uploaded_file is not None:
                # Vision Route: Handle Image Input
                image = Image.open(uploaded_file)
                prompt = f"Analyze this chat screenshot. Give me responses with a '{vibe}' vibe."
                response = model.generate_content([prompt, image])

                st.success("Analysis Complete.")
                st.write(response.text)

            elif user_message:
                # Text Route: Handle Text Input with Memory
                response = st.session_state.chat_session.send_message(user_message)

                st.success("Analysis Complete.")
                st.write(response.text)

            else:
                st.warning("You gotta give me a text or an image to work with, my friend.")

        except Exception as e:
            st.error(f"Something went wrong with the engine: {e}")