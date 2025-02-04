import openai
import streamlit as st
import os
import httpx
from openai import AzureOpenAI
from dotenv import dotenv_values
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
import text_to_sql_ai_bot as tx
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def settings():
    config = dotenv_values(".env")
    client = AzureOpenAI(
        azure_endpoint = config['azure_endpoint'],
        api_key=config['api_key'],  
        api_version="2024-08-01-preview",
        http_client = httpx.Client(verify=False),
        azure_deployment="gpt4o",
        
        
    ) 
    return client

def clickhouse_db():
    username = "default"
    password = ""
    host = "localhost"
    database = "hackathon"
    native_port = 9000
    engine = create_engine(
        f'clickhouse+native://{username}:{password}@{host}:' +
        f'{native_port}/{database}'
    )
    db = SQLDatabase(engine)
    return db

def process_query_result(query_result):
    """
    Process query result which is in the form of tuples and return a formatted dataframe.
    """
    if isinstance(query_result, list):
        # Check if the result is a list of tuples
        if all(isinstance(item, tuple) for item in query_result):
            # If it is a list of tuples, convert it to a DataFrame
            df = pd.DataFrame(query_result)
            return df
        else:
            # If it's a single value or a malformed result
            return pd.DataFrame(query_result, columns=["Result"])
    elif isinstance(query_result, tuple):
        # If it's a single tuple, convert it to a DataFrame
        return pd.DataFrame([query_result], columns=["Result"])
    else:
        # If it's some other data type, return as is
        return query_result
    
def display_result(query_result):
    """
    Display the query result as a table or graph depending on its structure.
    """
    # Process the query result
    df = process_query_result(query_result)
    
    if isinstance(df, pd.DataFrame):
        # If it's a DataFrame, display it in Streamlit
        st.dataframe(df)  # Display as table

        # Optionally, plot the data if it's numerical
        if df.shape[1] >= 1 and df.shape[1] <= 4:  # If there is only one column, assume it is a numerical series
            st.write("Displaying graph:")
            fig, ax = plt.subplots()
            ax.plot(df.iloc[:,0], df.iloc[:, 1], marker='o', linestyle='-', color='b')
            ax.set_title('Graph of Query Result')
            ax.set_xlabel(df.columns[0])
            ax.set_ylabel(df.columns[1])
            st.pyplot(fig)
        elif df.shape[1] >= 5:
            # Plot using Plotly for multi-column data
            if all(df.dtypes == df.dtypes[0]):
                st.write("Displaying plot:")
                fig = px.line(df, title="Query Result Over Time", labels={"index": "Index", "value": "Values"})
                st.plotly_chart(fig)
            else:
                # If columns have different types, we need to melt the DataFrame into a long format
                st.write("Displaying plot (reshaped data):")
                df_melted = df.reset_index().melt(id_vars='index', value_vars=df.columns, 
                                                    var_name='Variable', value_name='Value')
                fig = px.line(df_melted, x='index', y='Value', color='Variable', title="Query Result Over Time")
                st.plotly_chart(fig)
    else:
        st.write("Result:", df)

def validate_question(user_input):
    client = settings()
    db = clickhouse_db()
    context = db.get_context()
   
    prompt = f"""
            You are an intelligent assistant. Your task is to determine if a user's question can be converted into an SQL query to fetch data from a database. The database contains multiple tables with various attributes.

            To validate the user's question, follow these steps:
            1. Identify the key entities and attributes mentioned in the user's question.
            2. Check if these entities and attributes are present in the database schema.
            3. Determine if the question can be translated into a valid SQL query using the available tables and their relationships.
            4. If the question can be converted into an SQL query, respond with "Valid, the question can be converted to SQL."
            5. If the question is invalid, provide suggestions on how to frame valid questions and follow below instruction.
                - Politely explain that the question might be unclear or missing details.
                - Suggest the user clarify their question or provide more context, so that you can assist them better.
                - Mention that the question should be related to above table context.
                - Provide a helpful and supportive response such as: "Could you please provide more details or rephrase your question so I can assist you more effectively?"
                - Include a note that the question does not match the context of the available table information, which might include sales figures, trade performance, or similar metrics (without specific data or column names).
                - Include table information without any data or column just explaining it doesn't belong to table context
            Output should only include a helpful response explaining the clarification needed or why the question isn't valid

            **Example Database Schema:**
            {context["table_info"]}

            **Example User Questions:**
            1. "How many customers placed orders in 2023?"
            2. "What is the total amount spent by each customer?"

            **Example Validations:**
            1. Yes, the question is valid.
            2. Yes, the question is valid.

            Now, validate the following user question: "{user_input}"

    """

    response = client.chat.completions.create(
        model="gpt4o",  # You can use gpt-3.5-turbo or other models
        temperature=0,
        # stream=True,
        messages=[{"role": "user", "content": f"{prompt}"}],
    )

    for choice in response.choices:
        if any(keyword in choice.message.content.lower() for keyword in ["invalid", "not related", "unclear", "vague"]):
            st.write(choice.message.content)
            st.session_state.messages.append({"role": "assistant", "content": choice.message.content})
            return "Invalid question"
        else:
            return "Valid question"
            

st.set_page_config(page_title="Chat with the data", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)



def generate_insights(query_result,question):
    db = clickhouse_db()
    context = db.get_context()
    prompt = f"""
    User Question: {question}
    Here is the result for the above question:
    {query_result}
    Table Context:
    {context}

    Use the Table Context to provide the following suggestions:
    1. **Actionable Insights**: Based on the data, what are the key takeaways and important trends? What are the potential areas for improvement or focus?
    2. **Summary of Key Findings**: Provide a high-level summary of the key findings and their relevance to the original question.
    3. **Recommendations**: What actionable steps can the user take to address the findings or improve the situation based on the data?

    **Deep-Dive Suggestions**:
    - To gain a deeper understanding of the data, you can consider the following additional questions:
    - What factors might be contributing to the trends observed in the results? (e.g., seasonal patterns, geographic factors, etc.)
    - Are there any correlations between different variables in the data that could provide further insights? 
    - How does the performance vary over time or across different segments (e.g., by region, product category, or sales channel)?
    - Can we compare these results with past data or industry benchmarks to better understand the context and performance?
    
    These follow-up questions will help you dive deeper into the dataset and uncover more granular insights to inform your decisions.

    Feel free to ask more detailed questions based on the trends you see here, or to explore other aspects of the data for a better understanding of performance.
    """
    chat_client = settings()
    response = chat_client.chat.completions.create(
        model="gpt4o",  # You can use gpt-3.5-turbo or other models
        # prompt=prompt,
        temperature=0,
        stream=True,
        messages=[{"role": "user", "content": f"{prompt}"}],
    )
    
    st.write_stream(response)
    
    
   

import base64
import streamlit as st


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background: linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)),url("data:image/png;base64,%s") no-repeat center center/cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)



def chatbot():
    # chat_client = settings()
    # set_background('./images/img_12.jpg')
    st.title("Talks to Your data")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question about Sales or Trade Performance!"}
        ]

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt4o"


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about sales data or trade performance:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        print(st.session_state)

        with st.chat_message("assistant"):

            simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
            if prompt.lower() in simple_greetings:
                st.markdown("Hi there! Please ask a relevant question about sales or trade performance.")
                st.session_state.messages.append({"role": "assistant", "content": "Hi there! Please ask a relevant question about sales or trade performance."})
            else:
                validation_response = validate_question(prompt)
                #validation_response = "Valid question"
                print(validation_response)

                if  validation_response in ["Valid question"]:
                    query_result = tx.main(prompt)
                    
                    if query_result is not None:
                        if isinstance(query_result, str):
                            st.write(query_result)
                            st.session_state.messages.append({"role": "assistant", "content": query_result})
                        else:
                            display_result(query_result=query_result)

                        if len(query_result) !=0:
                            generate_insights(query_result,prompt)
                else:
                    st.session_state.messages.append({"role": "assistant", "content": validation_response})
                    print(st.session_state)


def main():
    chatbot()

if __name__ == "__main__":
    main()