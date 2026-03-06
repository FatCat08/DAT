import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.chat_models.tongyi import ChatTongyi
import re

# 加载环境变量
load_dotenv()

# ==========================================
# 1. 初始化一个测试用的 SQLite 数据库
# ==========================================
DB_URI = "sqlite:///test_sales.db"
engine = create_engine(DB_URI)
metadata = MetaData()

# 创建一张测试用的销售表
sales_table = Table(
    'sales_data', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('department', String, nullable=False),
    Column('product', String, nullable=False),
    Column('sales', Integer, nullable=False),
    Column('sale_date', String, nullable=False)  # 简单用字符串存日期 YYYY-MM-DD
)

metadata.create_all(engine)

# 插入一些测试数据
with engine.connect() as conn:
    # 简单的清理，防止重复插入
    conn.execute(sales_table.delete())
    conn.execute(sales_table.insert(), [
        {'department': 'HR', 'product': 'Software A', 'sales': 1000, 'sale_date': '2023-01-15'},
        {'department': 'IT', 'product': 'Software B', 'sales': 5000, 'sale_date': '2023-02-20'},
        {'department': 'Marketing', 'product': 'Ad Service', 'sales': 3000, 'sale_date': '2023-03-10'},
        {'department': 'IT', 'product': 'Hardware C', 'sales': 8000, 'sale_date': '2023-04-05'}
    ])
    conn.commit()

async def main():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("Error: DASHSCOPE_API_KEY is missing")
        return

    print("Initializing components...")
    
    # ==========================================
    # 2. 将数据库传递给 LangChain 的 SQLDatabase 包装器
    # ==========================================
    # 这个工具能自动读取所有表结构，并取几行作为 example
    db = SQLDatabase.from_uri(DB_URI, sample_rows_in_table_info=3)
    
    print("\n--- LangChain Extracted Schema Info ---")
    print(db.get_table_info())
    print("---------------------------------------")

    # ==========================================
    # 3. 初始化 Qwen3-Max LLM
    # ==========================================
    llm = ChatTongyi(
        model_name="qwen-max",
        dashscope_api_key=api_key,
        temperature=0
    )

    # ==========================================
    # 4. 创建 NL2SQL Chain
    # ==========================================
    # 这条链会自动将用户的自然语言提问 + db 的 schema 传递给大模型，生成能够执行的 SQL
    chain = create_sql_query_chain(llm, db)

    questions = [
        "请帮我查询 2023 年 IT 部门的总销售额是多少？",
        "所有部门中，哪一个部门的销售额最高？",
        "以图表所需的格式返回每个产品的销量分布数据"
    ]

    with open("sql_test_results.txt", "w", encoding="utf-8") as f:
        f.write("\n================ Testing NL2SQL ================\n")
        print("\n================ Testing NL2SQL ================")
        for q in questions:
            print(f"\n[User Query]: {q}")
            f.write(f"\n[User Query]: {q}\n")
            
            # 执行转换链
            response = await chain.ainvoke({"question": q})
            
            # 很多模型生成的 SQL 会包在 Markdown 中，你可以看到原生输出
            print(f"[Generated SQL]:\n{response}")
            f.write(f"[Generated SQL]:\n{response}\n")
            
            # Extract pure SQL using Regex matching everything from SELECT/select up to a semicolon
            sql = response
            if "```sql" in response:
                sql = response.split("```sql")[1].split("```")[0].strip()
            elif "SQLQuery:" in response:
                sql = response.split("SQLQuery:")[1].strip()
                if "```" in sql:
                    sql = sql.split("```")[0].strip()
            
            # Additional cleanup of trailing conversational text
            # Often LLMs append text after the query
            match = re.search(r'(?i)(SELECT[\s\S]*?;)', sql)
            if match:
                sql = match.group(1)
            else:
                # If no semicolon, just try to grab from SELECT to the end of lines that look like SQL
                match = re.search(r'(?i)(SELECT[\s\S]*)', sql)
                if match:
                    sql = match.group(1).split("\n\n")[0] # cut off trailing paragraphs

            sql = sql.strip()
            print(f"[Extracted Pure SQL]:\n{sql}")
            f.write(f"[Extracted Pure SQL]:\n{sql}\n")
            
            # 尝试放到数据库执行一下
            try:
                results = db.run(sql)
                print(f"[SQL Execution Result]: {results}")
                f.write(f"[SQL Execution Result]: {results}\n")
            except Exception as e:
                print(f"[SQL Execution Error]: {e}")
                f.write(f"[SQL Execution Error]: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
