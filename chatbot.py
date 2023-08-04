# Importing required packages
import streamlit as st
import openai
from absa import analysis

st.title("Chatting with ChatGPT")
st.sidebar.header("Instructions")
st.sidebar.info(
    '''This is a web application that allows to sentimenet analyse feedback you enter with 
       the OpenAI API's implementation of the ChatGPT model.
       Enter a **feedback** in the **text box** and **press enter** to receive 
       **sentiment analysis** from the ChatGPT
       '''
    )

# Set the model engine and your OpenAI API key
model_engine = "text-davinci-003"
openai.api_key = "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" #follow step 4 to get a secret_key

def main():
    '''
    This function gets the user input, pass it to ChatGPT function and 
    displays the response
    '''
    # Get user input
    user_query = st.text_input("Enter feedack here, to exit enter :q", "This product is good but the battery doesn't last. It's lightweight and very easy to use. Well worth the money")
    analysis_results=analysis(user_query)

    return st.write(f"{user_query} {analysis_results}")
# call the main function
main() 