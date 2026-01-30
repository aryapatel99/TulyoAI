

import streamlit as st
import base64
from google import genai

# ---- BACKGROUND IMAGE FUNCTION ----
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

    # -------------- STREAMLIT UI --------------
st.set_page_config(
    page_title="TULYO AI – Smart Decision & Comparison Assistant",
    page_icon="🤖",
    layout="wide"
)  





# ---- CALL BACKGROUND ----
add_bg_from_local("bg1.jpg")  # change if your file is .png


# -------------- CONFIGURE GEMINI CLIENT --------------
API_KEY = st.secrets["GEMINI_API_KEY"]
   # 🔴 put your real key here
MODEL_NAME = "gemini-2.5-flash"  # or any model that works for you

client = genai.Client(api_key=API_KEY)


# -------------- LOGIC FUNCTIONS --------------
def build_prompt(option_a, option_b, category, priorities, user_context):
    prompt = f"""
You are an AI decision assistant who helps users compare two options in REAL LIFE.
Your job is to produce a clean, SHORT, structured answer.

STRICT HTML RULES:
- Respond ONLY in HTML.
- Do NOT use Markdown symbols.
- Do NOT use ### or **bold**.
- Do NOT insert blank lines, empty lines, or <p></p> spacers in your response.
- Every element must come directly after the previous one with no empty space between them.
- Table must be clean and compact
- Don't ignore title of table in your response.

Here are the two options:

Option A: {option_a}
Option B: {option_b}

Category / Domain: {category}

The user cares most about: {priorities}

User additional context / situation: {user_context}

Please respond in this structure:

1. Short introduction (1–2 lines)
2. Pros of {option_a}
3. Cons of {option_a} 
4. Pros of {option_b} 
5. Cons of {option_b} 
6. Comparison summary in table form 
7. Final guidance:
   - When is {option_a} better?
   - When is {option_b} better?
   - Neutral note: "Final choice depends on user preferences."

Keep the language simple and clear, as if explaining to a completely new to this.
Use proper tables where needed and also use emojis to make interactive.
Do NOT give any direct medical or stock-buying advice.
pros and cons should be in tabular form
"""
    return prompt


def get_ai_comparison(option_a, option_b, category, priorities, user_context):
    prompt = build_prompt(option_a, option_b, category, priorities, user_context)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

def load_logo_base64(image_file, width=200):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    
    html = f"""
    <div style="text-align:center; margin-top:20px;">
        <img src="data:image/jpeg;base64,{encoded}" width="{width}">
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)



 

# Header
load_logo_base64("tulyo.jpeg", width=200)

st.markdown(
    "<h3 style='text-align:center; color:white;'>Smart Decision & Comparison Assistant</h3>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <h4 style="
        text-align:center; 
        color:white; 
        text-shadow: 0px 0px 10px rgba(255,255,255,0.8); 
        margin-top:-10px;
    ">
    ✨ Where real-life choices meet real AI solutions ✨
    </h4>
    """,
    unsafe_allow_html=True
)




st.markdown("---")

# Input area in two columns
col1, col2 = st.columns(2)

with col1:
    option_a = st.text_input("Option A", placeholder="e.g. This")

with col2:
    option_b = st.text_input("Option B", placeholder="e.g. That")

category = st.selectbox(
    "Category / Domain",
    ["Education", "Career", "Travel", "Lifestyle", "Finance (general info only)","Health","Purchase Decisions", "Other"]
)

priorities = st.text_input(
    "What matters most in this decision?",
    placeholder="e.g. money, time, comfort, learning, growth, safety, Quality, etc"
)

user_context = st.text_area(
    "Your situation (optional)",
    placeholder="e.g. I am a 1st year student, live 15 km from college, middle class family."
)

st.markdown("---")

# Button
if st.button("🔍 Compare with TULYO AI"):
    if not option_a or not option_b:
        st.warning("Please enter both Option A and Option B.")
    else:
        priorities_use = priorities if priorities else "Not specified"
        context_use = user_context if user_context else "Not specified"

        with st.spinner("Thinking... Tulyo AI is comparing your options..."):
            try:
                result = get_ai_comparison(
                    option_a,
                    option_b,
                    category,
                    priorities_use,
                    context_use
                )

                safe_result = result.replace("\n", "<br>")

                box_html = f"""
                <div style="
                     background-color: rgba(0, 0, 0, 0.85);
                     padding: 20px;
                     border-radius: 12px;
                     color: white;
                     font-size: 17px;
                     font-weight: bold;
                     line-height: 1.6;
                ">
                    <h3 style='text-align:center;'>📌 TULYO AI's comparison</h3>
                    <p>{safe_result}</p>
               </div>
               """

                st.markdown(box_html, unsafe_allow_html=True)



            except Exception as e:
                st.error("❌ Something went wrong while contacting the AI.")
                st.code(str(e))