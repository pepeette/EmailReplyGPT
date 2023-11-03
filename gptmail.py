# template = """
#     Below is an email that may be poorly worded.
#     Your goal is to:
#     - Properly format the email
#     - Convert the input text to a specified tone
#     - Convert the input text to a specified dialect

#     Here are some examples different Tones:
#     - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
#     - Informal: Went to Barcelona for the weekend. Lots to tell you.  

#     Here are some examples of words in different dialects:
#     - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
#     - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

#     Example Sentences from each dialect:
#     - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
#     - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.

#     Please start the email with a warm introduction. Add the introduction if you need to.
    
#     Below is the email, tone, and dialect:
#     TONE: {tone}
#     DIALECT: {dialect}
#     EMAIL: {email}
    
# """
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os
import openai
from dotenv import load_dotenv
load_dotenv() 

openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    try:
        openai.api_key = st.secrets['path']
    except st.secrets.SecretsFileNotFoundError:
        st.warning('Streamlit Secrets file not found. Please make sure you have set your secrets.')
        st.stop()

template = """
    Below is an email received from a Rockwoord Glass client or prospect.
    You are Rockwoord Glass company customer service representative,
    your goal is to:
    - Reply to this email in less than 150 words
    - Properly format the email response
    - Use an appropriate salesly, polite and concise tone
    - Make simple yet polite and accurate sentences 
    - Focus your email reply on the next action pending or done

    Please start the email with a warm introduction. Add the introduction if you need to.
    At Rockwoord Glass, we are number 1 bespoke design and manufacturing glass and ceramic bottles.
    We service the biggest names as well as the tailored demands. 
    
    Below is the email received with metadata :
    SENDER: {sender}
    RECIPIENT: {recipient}
    EMAIL: {email}
    

"""

prompt = PromptTemplate(
    input_variables=["sender", "recipient","email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai.api_key)
    return llm

st.set_page_config(page_title=" RockwoodGPT 📩 ", page_icon=":robot:")

# Use HTML to center the title
st.write("""
    <div style="display: flex; align-items: center; justify-content: center;">
        <img src="https://www.rockwoodglass.com/wp-content/uploads/2020/02/logo.png" alt="RWlogo" style="width: 50px; height: 50px;">
        <h2 style="margin-left: 10px;">📩 RockWood Email Generator</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([12, 12])
with col1:
    sender = st.text_input(label="Name of the client", key="sender_input")
with col2:
    st.text("Type of client (or select from options)")
    col2_1, col2_2 = st.columns([1, 3])
    with col2_1:
        typology_input = st.text_input("Type or ->", key="typology_input")    
    with col2_2:
        typology_options = ["Enquiry", "Professional", "Unprofessional", "Idiot", "Arsey"] 
        typology = st.selectbox("Select from options", typology_options)

def get_text():
    input_text = st.text_area(label="Paste the email here",  placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

col3, col4 = st.columns([12, 12])
with col3:
    tone = st.text_input(label="Response tone", key="tone_input")
with col4:
    recipient = st.text_input(label="Your name", key="recipient_input")

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

if st.button("Generate REPLY", type='secondary', help="Click to see an example of the email you will be creating."):

    if email_input and sender and recipient:
        if not openai.api_key:
            st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
            st.stop()

        llm = load_LLM(openai_api_key=openai.api_key)

        prompt_with_email = prompt.format(sender=sender, recipient=recipient, email=email_input)

        formatted_email = llm(prompt_with_email)

        st.write(formatted_email)

