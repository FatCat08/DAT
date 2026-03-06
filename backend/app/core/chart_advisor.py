import json
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from app.config import get_settings

class ChartAdvisor:
    def __init__(self):
        self.settings = get_settings()
        self.llm = ChatTongyi(
            model_name="qwen-max",
            dashscope_api_key=self.settings.DASHSCOPE_API_KEY,
            temperature=0
        )
        
        self.prompt = PromptTemplate.from_template(
            """You are a data visualization expert.
Given a user's original question and the structured SQL data result, recommend the best ECharts visual configuration.
If the data cannot be charted at all (e.g. counting a single number), respond with `{{"chartType": "none"}}`. However, ALWAYS prioritize generating a chart if two or more columns of data are present.

<User Question>
{question}
</User Question>

<Data Schema>
Columns: {columns}
Rows (first 5 samples): {sample_rows}
</Data Schema>

Your JSON output MUST match exactly this structure, and NOTHING ELSE:
{{
  "chartType": "bar", // Choose one of: bar, line, pie, scatter, none
  "title": "A short descriptive title",
  "xAxis": "exact column name for X axis",
  "yAxis": "exact column name for Y axis",
  "valueColumn": "exact column name for pie slices",
  "nameColumn": "exact column name for pie labels"
}}

Output ONLY valid JSON:
"""
        )
        
        self.chain = self.prompt | self.llm
        
    async def recommend_chart(self, question: str, columns: list, rows: list) -> dict:
        """Asks Qwen to recommend an Echarts configuration based on data shape."""
        # Don't send massive data, just the first 5 rows for context
        sample_rows = rows[:5] if rows else []
        
        if not rows or not columns:
            return {"chartType": "none"}
            
        try:
            response = await self.chain.ainvoke({
                "question": question,
                "columns": str(columns),
                "sample_rows": str(sample_rows)
            })
            
            # Clean up potential markdown from LLM
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            print(f"Chart Advisor error: {e}")
            return {"chartType": "none"}
