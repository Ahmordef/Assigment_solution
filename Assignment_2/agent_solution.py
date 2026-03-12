import os
import requests
from google.colab import userdata
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent  # ✅ التعديل الأول: استدعاء الدالة الجديدة
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage

# 1. سحب المفاتيح
os.environ["OPENROUTER_API_KEY"] = userdata.get('OPENROUTER_API_KEY')
os.environ["TAVILY_API_KEY"] = userdata.get('TAVILY_API_KEY')

# 2. تعريف أداة قراءة المواقع (fetch_url)
@tool
def fetch_url(url: str) -> str:
    """Fetch text content from a URL to get detailed information."""
    try:
        response = requests.get(url, timeout=10.0)
        response.raise_for_status()
        return response.text[:5000] # نأخذ أول 5000 حرف فقط
    except Exception as e:
        return f"Error fetching {url}: {str(e)}"

# 3. تعريف أداة البحث (internet_search) لـ 3 نتائج
internet_search = TavilySearchResults(max_results=3)

# 4. إعداد نموذج الذكاء الاصطناعي
llm = ChatOpenAI(
    model="nvidia/nemotron-3-nano-30b-a3b:free",
    temperature=0,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

# 5. إعطاء التعليمات للعميل
AGENT_PROMPT = """You are an expert researcher. 
Your task is to:
1. Refine the user's query if needed.
2. Use the search tool to find the top 3 ranking sites.
3. Use 'fetch_url' to read the content of those URLs.
4. Provide a final, concise answer based ONLY on what you read."""

# 6. بناء العميل الذكي (التعديل الثاني: استخدام system_prompt)
tools = [internet_search, fetch_url]
agent = create_agent(model=llm, tools=tools, system_prompt=AGENT_PROMPT)

print("✅ تم بناء العميل بنجاح! جاري البحث والتفكير...\n" + "="*50)

# 7. اختبار العميل
result = agent.invoke({
    "messages": [
        HumanMessage("What are the latest updates in LangGraph in 2025?")
    ]
})

# طباعة الإجابة النهائية
print(result["messages"][-1].content)
