# Assignment 1: Case Study Presentation

### Slide 1: Overview & Personal Information
* **Company:** Captide
* **Industry:** Software & Technology (Fintech / Equity Research)
* **Use Case:** Agentic Workflows for Data Extraction and Financial Analysis.
* **Reference:** [LangChain Case Study (2025)](https://blog.langchain.dev/how-captide-is-redefining-equity-research-with-agentic-workflows-built-on-langgraph-and-langsmith/)
* **Student Name:** [اكتب اسمك هنا]
* **University:** [اكتب اسم جامعتك هنا]
* **Department / Major:** [اكتب تخصصك هنا]

---

### Slide 2: The Problem Statement
* **Complexity:** Financial documents (Earnings reports) are huge, inconsistent, and highly technical.
* **Limitation of Old Systems:** Traditional "chains" (Linear workflows) couldn't handle errors or complex table structures, leading to inaccurate financial data extraction.

---

### Slide 3: The "Agentic" Components (The LLM Brain)
*What makes this system an "Agent" and not just a script?*
* **Reasoning & Decision Making:** The agent looks at the document and decides which "tool" to use based on the content.
* **Self-Correction (The Loop):** If the extracted numbers don't balance (e.g., Assets ≠ Liabilities), the agent "re-reads" the document to find the error.
* **Dynamic Routing:** The agent chooses different paths for a "Press Release" vs. a "10-K Report" without manual coding.

---

### Slide 4: The "Non-Agentic" Components (Traditional Software)
*Crucial components that do NOT use LLMs:*
* **PDF Parsing Engine:** Hard-coded libraries (like PyMuPDF) used to turn PDF pixels into raw text.
* **Schema Validation:** Standard Python code (Pydantic) that checks if data types are correct.
* **Database Storage:** Traditional SQL or Vector databases that store information using fixed algorithms.

---

### Slide 5: Why LangGraph? (Conclusion)
* **Control over Cycles:** LangGraph allows the agent to "loop back" and retry if a task fails.
* **State Management:** It keeps track of the data history throughout the process.
* **Human-in-the-loop:** It allows a human analyst to review and "approve" the work at critical steps.


  ---

## Assignment 2: Building an Agentic AI System

### 🎯 Task Overview
Create a research agent that refines a user query, searches the web, and reads the top 3 ranking sites to provide a comprehensive and grounded answer.

### 🛠️ Tools & Frameworks
* **Search Tool:** `TavilySearchResults` (to find the top 3 links).
* **Scraping Tool:** Custom `fetch_url` tool (to read raw text from the retrieved URLs).
* **LLM:** NVIDIA Nemotron-3-nano-30b (via OpenRouter).
* **Orchestration:** LangChain & LangGraph (`create_agent`).

### 💻 Code Solution
The complete Python script for this agent can be found here: [agent_solution.py](./Assignment_2/agent_solution.py)

### 📈 Execution Output (Proof of Work)
**User Query:** *"What are the latest updates in LangGraph in 2025?"*

**Agent Response:**
> **Latest LangGraph updates in 2025 (based on the search results):**
> 
> * **August 2025 – Prompt‑engineering UI:** View and edit node logic directly in LangGraph Studio.
> * **May 2025 – Node‑level caching & Deferred nodes:** Cache task results to speed up execution and support running nodes only after parallel branches complete.
> * **May 2025 – MCP & Swarm library:** Reliable connection to remote MCP servers and a lightweight library for building multi‑agent swarms.
> * **March 2025 – "BigTool" library:** Allows agents to access a large number of tools scalably.
> * **March 2025 – Pre‑built agents (LangGraph 0.3):** Templates for developers to control complex workflows easily.
