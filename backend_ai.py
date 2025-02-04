from sqlalchemy import create_engine
from sqlalchemy import text
from langchain_community.utilities import SQLDatabase

from langchain.chains.sql_database.prompt import SQL_PROMPTS

from langchain.chains import create_sql_query_chain
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import RunnableLambda
from dotenv import dotenv_values
import httpx
import re 
import pandas as pd
from openai import AzureOpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate   

from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import ast
from datetime import datetime,date


def main(question):
    try:
        list(SQL_PROMPTS)
        config = dotenv_values(".env")

        username = "default"
        password = ""
        host = "localhost"
        secure = False
        database = "hackathon"
        native_port = 9000
       
        engine = create_engine(
            f'clickhouse+native://{username}:{password}@{host}:' +
            f'{native_port}/{database}'
        )

        llm = AzureChatOpenAI(
            azure_deployment="gpt4o",
            api_version="2024-08-01-preview",
            temperature=0,
            azure_endpoint=config['azure_endpoint'],
            api_key=config['api_key'],
            http_client=httpx.Client(verify=False),
        )


        db = SQLDatabase(engine)

        print(db.dialect)
        print(db.get_usable_table_names())

        

        chain=create_sql_query_chain(llm,db)
        chain.get_prompts()[0].pretty_print()
        context = db.get_context()
        print(list(context))
        print(context["table_info"])
        prompt_with_context = chain.get_prompts()[0].partial(table_info=context["table_info"])
        print(prompt_with_context.pretty_repr())
       

        system = """
            Double check the user's {dialect} query for common mistakes, including:
                - Only return SQL Query not anything else like ```sql ... ```, ```Questions:```
                - Using NOT IN with NULL values
                - Using UNION when UNION ALL should have been used
                - Using BETWEEN for exclusive ranges
                - Data type mismatch in predicates\
                - Using the correct number of arguments for functions
                - Casting to the correct data type
                - Using the proper columns for joins

                - Ensure no `NULL` values are included with `NOT IN`.
                - Use `UNION ALL` instead of `UNION` when duplicates are acceptable.
                - Avoid exclusive range issues with `BETWEEN`.
                - Ensure correct data types for comparisons and predicates.
                - Ensure proper joins and valid column references.

                If there are any of the above mistakes, rewrite the query.
                If there are no mistakes, just reproduce the original query with no further commentary.
                Ensure the query is compatible with clickhouse database


                Output the final corrected SQL query only."""
        
        system = system + f"""
            Use following table information while genarating sql 
            Table Context:
            {context["table_info"]}
            - Datetime column is timestamp column it contains both date and time
            - Ensure proper handling of DateTime columns. If comparing DateTime columns, use toDate() or similar functions to normalize them and avoid errors. If date-only comparison is needed, cast both sides to Date to ignore the time component.

            Output the final SQL query only
        """
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{query}")]).partial(dialect=db.dialect)
        validation_chain = prompt | llm | StrOutputParser()
        full_chain = {"query": chain} | validation_chain
        user_question = question
        # user_question = "give me a trend of month on month sales"
        query = full_chain.invoke({"question":f"{user_question}"})
        print(query)
        output = db.run(query,include_columns=True)
        print(output)
        # df = pd.DataFrame(output)
        print(type(output))
        if len(output) != 0:
            if isinstance(output,str):
                output_data = output.replace("datetime.date", "date")
                output_data=eval(output_data)
            else:
                output_data=output
            df = pd.DataFrame(output_data)
            print(df)
            return df
        else:
            df = pd.DataFrame()


    except Exception as ex:
        print(ex)
        return "Invalid Question or Erro"
