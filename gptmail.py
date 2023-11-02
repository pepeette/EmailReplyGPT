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

col1, col2 = st.columns([10, 10])
with col1:
    sender = st.text_input(label="Sender's Name", key="sender_input")
with col2:
    recipient = st.text_input(label="Recipient's Name", key="recipient_input")

def get_text():
    input_text = st.text_area(label="Paste the email here",  placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

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
