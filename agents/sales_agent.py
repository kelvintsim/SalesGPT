import json
from langchain.chat_models import AzureChatOpenAI
from salesgpt.agents import SalesGPT
import streamlit as st
import os

#initialize agent
def init():
    llm = AzureChatOpenAI(deployment_name = os.environ["DEPLOYMENT_NAME"])
    #config sales agent
    file = open("agent_setup.json", "r")
    config=json.load(file)
    sales_agent = SalesGPT.from_llm(llm, verbose=False, **config)
    sales_agent.seed_agent()
    sales_agent.step()
    return sales_agent

def get_generated_message(agent, input_text, history):
    agent.human_step(input_text)
    agent.conversation_history = history
    agent.step()
    generated_message = agent.conversation_history[-1][:-13]
    return generated_message

def get_latest_message(agent):
    return agent.conversation_history[-1]

def get_clean_message(message):
    return message[:-13]