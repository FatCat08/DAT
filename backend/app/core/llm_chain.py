import json
import asyncio
from typing import AsyncGenerator
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

from app.config import get_settings
from app.core.sql_agent import SQLAgent
from app.core.chart_advisor import ChartAdvisor
from app.services.session_service import SessionService

@tool
def query_database(query_description: str) -> str:
    """Useful for when you need to answer questions about sales, departments, or product data.
    Provide a detailed description of what data needs to be pulled.
    """
    pass

class LLMChain:
    def __init__(self, session_service: SessionService):
        self.settings = get_settings()
        self.session_service = session_service
        self.sql_agent = SQLAgent()
        self.chart_advisor = ChartAdvisor()
        
        self.llm = ChatTongyi(
            model_name="qwen-max",
            dashscope_api_key=self.settings.DASHSCOPE_API_KEY,
            temperature=0.2,
            streaming=True
        )
        # Bind the specific tool for data queries
        self.llm_with_tools = self.llm.bind_tools([query_database])

    async def generate_response_stream(
        self, session_id: str, new_user_message: str
    ) -> AsyncGenerator[str, None]:
        """Orchestrates the LLM workflow and yields Server-Sent Events (SSE)."""
        
        # 1. Save user message to DB
        await self.session_service.save_message(session_id, "user", new_user_message)
        
        # 2. Get conversation history (last 10 rules)
        session_detail = await self.session_service.get_session_detail(session_id)
        messages_history = session_detail.messages[-10:]
        
        # Build Langchain memory format
        langchain_msgs = [SystemMessage(content="You are a helpful Data Assistant.")]
        for msg in messages_history[:-1]:  # exclude the one we just appended manually to avoid duplicate
            if msg.role == 'user':
                langchain_msgs.append(HumanMessage(content=msg.content))
            else:
                langchain_msgs.append(AIMessage(content=msg.content))
        langchain_msgs.append(HumanMessage(content=new_user_message))

        metadata_buffer = {}
        ai_response_content = ""
        
        # 3. Intent Recognition with bind_tools
        initial_response = await self.llm_with_tools.ainvoke(langchain_msgs)
        
        if initial_response.tool_calls:
            # IT'S A DATA QUERY!
            tool_call = initial_response.tool_calls[0]
            if tool_call["name"] == "query_database":
                # A: Generate SQL
                sql_query = await self.sql_agent.generate_sql(new_user_message)
                yield f"event: sql\ndata: {json.dumps({'sql': sql_query})}\n\n"
                metadata_buffer["sql"] = sql_query
                
                # B: Execute SQL
                exec_result = self.sql_agent.execute_sql(sql_query)
                yield f"event: data\ndata: {json.dumps(exec_result)}\n\n"
                metadata_buffer["data"] = exec_result
                
                # C: Generate Chart config
                if not exec_result.get("error") and exec_result.get("rows"):
                    chart_json = await self.chart_advisor.recommend_chart(
                        new_user_message, 
                        exec_result["columns"], 
                        exec_result["rows"]
                    )
                    yield f"event: chart\ndata: {json.dumps(chart_json)}\n\n"
                    metadata_buffer["chart"] = chart_json
                    
                # D: Streaming text explanation/summary
                summary_prompt = langchain_msgs + [
                    AIMessage(content="", tool_calls=[tool_call]),
                    HumanMessage(content=f"Tool executed. Raw data result: {exec_result}. Summarize this for me cleanly.")
                ]
                
                # We use regular llm here because we want an actual stream of text
                async for chunk in self.llm.astream(summary_prompt):
                    if chunk.content:
                        ai_response_content += chunk.content
                        yield f"event: text_delta\ndata: {json.dumps({'content': chunk.content})}\n\n"
                
        else:
            # REGULAR CHAT! Use astream directly.
            async for chunk in self.llm.astream(langchain_msgs):
                if chunk.content:
                    ai_response_content += chunk.content
                    yield f"event: text_delta\ndata: {json.dumps({'content': chunk.content})}\n\n"

        # 4. Save AI Response to DB
        saved_msg = await self.session_service.save_message(
            session_id, 
            "assistant", 
            ai_response_content,
            metadata=metadata_buffer if metadata_buffer else None
        )
        
        # 5. Signal Completion
        yield f"event: done\ndata: {json.dumps({'message_id': saved_msg.id})}\n\n"
