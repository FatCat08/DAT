import os
import asyncio
import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

load_dotenv()

@tool
def query_database(sql_query: str) -> str:
    """Execute a SQL query on the database and return the results."""
    return f"Results for: {sql_query}"

@tool
def suggest_chart(chart_type: str, x_axis: str, y_axis: str) -> str:
    """Suggest a chart based on the data."""
    return f"Chart suggested: {chart_type} with x={x_axis}, y={y_axis}"

async def main():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    llm = ChatTongyi(
        model_name="qwen-max",
        dashscope_api_key=api_key,
        temperature=0
    )
    llm_with_tools = llm.bind_tools([query_database, suggest_chart])
    messages = [HumanMessage(content="请帮我查询数据库中2023年各部门的销售额，并建议用柱状图展示，x轴为部门，y轴为销售额。")]
    
    response = await llm_with_tools.ainvoke(messages)
    
    out_dict = {
        "content": response.content,
        "tool_calls": response.tool_calls,
        "additional_kwargs": response.additional_kwargs
    }
    
    with open("qwen_dump.json", "w", encoding="utf-8") as f:
        json.dump(out_dict, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
