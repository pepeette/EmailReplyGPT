# template = """
#     Below is an email that may be poorly worded.
#     Your goal is to:
#     - Properly format the email
#     - Convert the input text to a specified tone
#     - Convert the input text to address a specific typology

#     Here are some examples different Tones:
#     - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
#     - Informal: Went to Barcelona for the weekend. Lots to tell you.  

#     Here are some examples of words in different typology:
#     - Arsey: He thinks he knows better and is inpolite, the best reponse to this typology is to name drop, 
#    state that we serve the best clients, that we do and we know what we do, we are the expert, respond in expert tone
#     - Eqnuiry: He wants more information, we need to respond in short and informative way, name dropping that we are the best, 
#    respond in informative tone

#     Please start the email with a warm introduction. Add the introduction if you need to.
    
#     Below is the email, tone, and typology of client:
#     TONE: {tone}
#     TYPOLOGY: {typology}
#     EMAIL: {email}
    
# """
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import os
import openai
from PIL import Image
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
    Below is an email received from a Rockwoord Glass client or prospect called {sender}.
    You, {recipient}, are Rockwoord-Glass company customer service representative,
    your goal is to reply to this email received in an email formatted manner.
    Do write the reply bearing in mind these strict requirements : 
    - Reply in less than 150 words
    - Properly format the email response
    - Use the appropriate tone : {tone} for the client typology : {typology}
    - Make very simple sentences. Use bullet points when appropriate.
    - Focus the reply on the next action.

    Please start the email with a short and warm introduction. Add the introduction if you need to.
    At Rockwoord Glass, we are number 1 bespoke design and manufacturing glass and ceramic bottles.
    We service the biggest names as well as the tailored demands. 
    
    Here is the email received to reply to :
    EMAIL RECEIVED: {email}
    

"""

prompt = PromptTemplate(
    input_variables=["sender", "typology","tone","recipient","email"],
    template=template,
)

def load_LLM(openai_api_key):
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai.api_key)
    return llm

st.set_page_config(page_title=" RockwoodGPT 📩 ", page_icon=":robot:")

#TITLE
image = Image.open('logo.png')
colA, colB = st.columns([1, 3])
with colA:
    st.image(image)
with colB:
    st.header("  RockWood Email Generator ")

st.write(" ")
st.write(" ")
st.write(" ")


#LOGIC
col1, col2 = st.columns([6, 12])
with col1:
    sender = st.text_input(label="Name of the client *", key="sender_input")
with col2:
    #st.write("Indicate the sender's typology")
    row1, row2 = st.columns(2)

    with row1:
        typology_input = st.text_input("Type of client", placeholder="Type", key="typology_input")
        
    with row2:
        typology_options = ["Enquiry", "Professional", "Unprofessional", "Idiot", "Arsey"]

        # Check if the text input is not empty
        if typology_input:
            typology = typology_input
        else:
            # If text input is empty, use the dropdown or set typology to None
            typology = st.selectbox("(or select from options)", typology_options, index=None, key="typology_select", placeholder="Select ..")


def get_text():
    input_text = st.text_area(label="Paste the email received here *",  placeholder="Your Email...", key="email_input")
    return input_text
    
email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

col3, col4 = st.columns([12, 12])
with col3:
    tone_options = ["Informative","Salesly","Polite","Monopolistic","Expert"]
    tone = st.selectbox("", tone_options, index=None, key="tone_select", placeholder="Select tone to reply")
with col4:
    recipient = st.text_input(label="Your name *", key="recipient_input")


st.write(" ")

#MAIN
if st.button("Generate REPLY 📩", type='secondary', help="Click to see an example of the email you will be creating."):

    if email_input and sender and recipient:
        if not openai.api_key:
            st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
            st.stop()

        llm = load_LLM(openai_api_key=openai.api_key)

        prompt_with_email = prompt.format(
            sender=sender,
            recipient=recipient,
            email=email_input,
            typology=typology if 'typology' in locals() else 'None',
            tone=tone if 'tone' in locals() else 'None',
        )

        formatted_email = llm(prompt_with_email)

        st.write(formatted_email)
    else:
        st.warning('Please fill in all required fields (Name of the client, Your name, and paste the email).', icon="⚠️")
