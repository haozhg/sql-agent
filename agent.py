import os
import argparse

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI

def parse_args():
    argparser = argparse.ArgumentParser(description="SQL Agent")
    
    argparser.add_argument(
        "--sqlite_uri",
        type=str,
        default="sqlite:///fifa.db"
    )
    return argparser.parse_args()
    
    
def main():
    args = parse_args()
    print("I am a SQL Agent to help you answer questions about a database, as well as recover from errors")
    print("You can ask questions like: Describe the `fifa` table")
    
    if not os.environ["OPENAI_API_KEY"]:
        raise Exception("You need to run export OPENAI_API_KEY=your_openai_api_key")
    
    db = SQLDatabase.from_uri(args.sqlite_uri)
    # llm=OpenAI(temperature=0)
    llm=ChatOpenAI(temperature=0)
    print(f"llm.model_name={llm.model_name}")
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )
    while True:
        user_input = input("User Input: ")
        try:
            agent_executor.run(user_input)
        except Exception as e:
            print(f"{e}")
            print("Please try a different question")
    
if __name__ == "__main__":
    main()