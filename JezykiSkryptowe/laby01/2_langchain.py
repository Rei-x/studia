import streamlit as st
from langchain import hub
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain_openai import OpenAI

llm = OpenAI(temperature=0, streaming=True)

tools = load_tools(["google-serper"])
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)  # type: ignore

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())

        response = agent_executor.invoke(
            {"input": prompt}, {"callbacks": [st_callback]}
        )

        st.write(response["output"])
