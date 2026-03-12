!pip install -q langchain langchain_openai langchain_community langgraph

import os
from google.colab import userdata  # <--- هذا هو السطر الذي يحل المشكلة
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

# ==========================================
# 0. سحب المفتاح من بيئة Colab (الخطوة الأهم)
# ==========================================
os.environ["OPENROUTER_API_KEY"] = userdata.get('OPENROUTER_API_KEY')

# إعداد النموذج
llm = ChatOpenAI(
    model="nvidia/nemotron-3-nano-30b-a3b:free",
    temperature=0,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

# ==========================================
# 1. تعريف الأدوات الأساسية (Tools)
# ==========================================

@tool
def log_incident_to_sql(incident_type: str, severity: str, location: str) -> str:
    """Log the incident details into the official SQL risk register database."""
    return f"SUCCESS: Incident '{incident_type}' (Severity: {severity}) at '{location}' logged to SQL database."

@tool
def search_liferay_cms(query: str) -> str:
    """Search the Liferay Content Management System for Business Continuity Plans and Governance Protocols."""
    return f"Liferay CMS Result: For '{query}', the business continuity protocol requires activating backup generators within 15 minutes and notifying the IT ops team."

@tool
def send_emergency_alert(department: str, message: str, level: str) -> str:
    """Send SMS and email emergency broadcasts to specific departments."""
    return f"Broadcast Sent to {department} [Level: {level}]: {message}"

# ==========================================
# 2. إنشاء الوكلاء الفرعيين (Sub-Agents)
# ==========================================

incident_agent = create_agent(
    model=llm,
    tools=[log_incident_to_sql],
    system_prompt="You are an Incident Logging Specialist. Extract incident type, severity, and location from the request and log it using the SQL tool. Always confirm the logged details."
)

governance_agent = create_agent(
    model=llm,
    tools=[search_liferay_cms],
    system_prompt="You are a Governance & Compliance Specialist. Search the Liferay CMS for relevant business continuity protocols based on the incident description and summarize the required actions."
)

broadcast_agent = create_agent(
    model=llm,
    tools=[send_emergency_alert],
    system_prompt="You are an Emergency Communications Specialist. Draft concise, urgent alerts and use the broadcast tool to send them to the appropriate departments."
)

# ==========================================
# 3. تغليف الوكلاء كأدوات (Wrap Sub-agents as Tools)
# ==========================================

@tool
def manage_incident_logging(request: str) -> str:
    """Use this to extract incident details and log them into the SQL risk database. Input should be the incident description."""
    result = incident_agent.invoke({"messages": [HumanMessage(request)]})
    return result["messages"][-1].content

@tool
def query_governance_protocols(request: str) -> str:
    """Use this to search the Liferay CMS for business continuity plans and governance rules. Input should be the incident type."""
    result = governance_agent.invoke({"messages": [HumanMessage(request)]})
    return result["messages"][-1].content

@tool
def handle_emergency_broadcasts(request: str) -> str:
    """Use this to draft and send SMS/email emergency alerts to affected departments. Input should include severity and details."""
    result = broadcast_agent.invoke({"messages": [HumanMessage(request)]})
    return result["messages"][-1].content

# ==========================================
# 4. إنشاء الوكيل المشرف (Supervisor Agent)
# ==========================================

SUPERVISOR_PROMPT = """You are the Chief Risk Coordinator (Supervisor). 
You manage institutional incidents by coordinating three specialists:
1. 'manage_incident_logging' to record the event.
2. 'query_governance_protocols' to find the official response plan.
3. 'handle_emergency_broadcasts' to alert the staff.

Break down the user's incident report, call the necessary tools in sequence, and provide a final synthesized report of all actions taken.
"""

supervisor_agent = create_agent(
    model=llm,
    tools=[manage_incident_logging, query_governance_protocols, handle_emergency_broadcasts],
    system_prompt=SUPERVISOR_PROMPT
)

# ==========================================
# 5. اختبار النظام (Execution)
# ==========================================
print("🚨 Simulating Incident Report...\n")
incident_report = "There is a major power outage in the main server room. It is highly critical."

# تشغيل المشرف
result = supervisor_agent.invoke({"messages": [HumanMessage(incident_report)]})

print("✅ Final Supervisor Report:")
print("="*50)
print(result["messages"][-1].content)
