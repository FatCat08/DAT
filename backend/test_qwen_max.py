import os
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

# 加载环境变量
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
    if not api_key:
        print("Error: DASHSCOPE_API_KEY is missing in .env")
        return

    print("Initializing ChatTongyi (qwen-max)...")
    # 使用 Qwen Max 模型
    llm = ChatTongyi(
        model_name="qwen-max",
        dashscope_api_key=api_key,
        temperature=0
    )
    
    # 测试 1: 流式输出 (Streaming)
    print("\n" + "="*40)
    print("Test 1: Streaming Output")
    print("="*40)
    print("Assistant: ", end="", flush=True)
    try:
        async for chunk in llm.astream("请用中文讲一个关于程序员的很短的冷笑话。"):
            print(chunk.content, end="", flush=True)
        print("\n")
    except Exception as e:
        print(f"\n[Streaming Error]: {e}")

    # 测试 2: 函数调用 (Tool Calling)
    print("\n" + "="*40)
    print("Test 2: Tool Calling (Function Calling)")
    print("="*40)
    
    # 绑定工具
    llm_with_tools = llm.bind_tools([query_database, suggest_chart])
    
    # 发送包含明确工具调用意图的消息
    messages = [
        HumanMessage(content="请帮我查询数据库中2023年各部门的销售额，并建议用什么图表展示最好。")
    ]
    
    try:
        response = await llm_with_tools.ainvoke(messages)
        
        print(f"Text Response Content: {repr(response.content)}")
        print("\nFunction/Tool Calls Extracted by LangChain:")
        if not response.tool_calls:
            print("No tool calls found in the response.")
            
        for idx, tc in enumerate(response.tool_calls):
            print(f"\nTool Call #{idx + 1}:")
            print(f"  - Name (函数名): {tc['name']}")
            print(f"  - Args (参数字典): {tc['args']}")
            print(f"  - ID: {tc['id']}")
            
        print("\nRaw Message Additional kwargs (真实返回结构):")
        print(response.additional_kwargs)
            
    except Exception as e:
        print(f"\n[Tool Calling Error]: {e}")

if __name__ == "__main__":
    asyncio.run(main())
