!pip install -q langchain langchain-community langchain-openai langchain-huggingface sentence-transformers langgraph
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.5/2.5 MB 29.5 MB/s eta 0:00:00
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 87.7/87.7 kB 7.4 MB/s eta 0:00:00
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.0/1.0 MB 60.7 MB/s eta 0:00:00
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.7/64.7 kB 6.5 MB/s eta 0:00:00
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 51.0/51.0 kB 4.7 MB/s eta 0:00:00
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
google-colab 1.0.0 requires requests==2.32.4, but you have requests 2.32.5 which is incompatible.

import os
from google.colab import userdata
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

# ==========================================
# 0. Setup API Key
# ==========================================
os.environ["OPENROUTER_API_KEY"] = userdata.get('OPENROUTER_API_KEY')

# ==========================================
# 1. Create a NEW Data Source (Machine Learning History)
# ==========================================
ml_history = """
Machine Learning History & Milestones

1. Early Foundations
The term "machine learning" was coined by Arthur Samuel in 1959 while he was at IBM. He developed a computer program for playing checkers that could learn from its mistakes.

2. The Perceptron
In 1958, psychologist Frank Rosenblatt invented the Perceptron, an early artificial neural network. It was initially implemented in hardware rather than software and was designed for image recognition.

3. The Deep Learning Era and Backpropagation
While neural networks faced a "winter", they were revived in the 1980s. In 1986, David Rumelhart, Geoffrey Hinton, and Ronald Williams popularized the backpropagation algorithm, which is essential for training deep neural networks with multiple layers.
"""

# حفظ النص في ملف محلي جديد
with open("ml_history.txt", "w", encoding="utf-8") as f:
    f.write(ml_history)

# ==========================================
# 2. Load and Split
# ==========================================
loader = TextLoader("ml_history.txt")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
all_splits = text_splitter.split_documents(docs)

# ==========================================
# 3. Embed and Store
# ==========================================
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents(documents=all_splits)
 /usr/local/lib/python3.12/dist-packages/huggingface_hub/utils/_auth.py:94: UserWarning: 
The secret `HF_TOKEN` does not exist in your Colab secrets.
To authenticate with the Hugging Face Hub, create a token in your settings tab (https://huggingface.co/settings/tokens), set it as secret in your Google Colab and restart your session.
You will be able to reuse this secret in all of your notebooks.
Please note that authentication is recommended but still optional to access public models or datasets.
  warnings.warn(
modules.json: 100% 349/349 [00:00<00:00, 36.7kB/s]config_sentence_transformers.json: 100% 116/116 [00:00<00:00, 14.6kB/s]README.md:  11.6k/? [00:00<00:00, 1.48MB/s]sentence_bert_config.json: 100% 53.0/53.0 [00:00<00:00, 5.24kB/s]config.json: 100% 571/571 [00:00<00:00, 75.2kB/s]model.safetensors: 100% 438M/438M [00:05<00:00, 197MB/s]Loading weights: 100% 199/199 [00:00<00:00, 645.55it/s, Materializing param=pooler.dense.weight]MPNetModel LOAD REPORT from: sentence-transformers/all-mpnet-base-v2
Key                     | Status     |  | 
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
tokenizer_config.json: 100% 363/363 [00:00<00:00, 50.2kB/s]vocab.txt:  232k/? [00:00<00:00, 11.8MB/s]Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
WARNING:huggingface_hub.utils._http:Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
tokenizer.json:  466k/? [00:00<00:00, 23.8MB/s]special_tokens_map.json: 100% 239/239 [00:00<00:00, 32.2kB/s]config.json: 100% 190/190 [00:00<00:00, 21.0kB/s]['308e397f-efd2-4ad8-b200-5c4b23696473',
 '186a8393-cbac-4f38-9b67-6197fb5aaa68',
 '6137ebe3-822e-48ec-a956-f63fbef2bf39',
 '60c1a1ba-1148-4a27-99f6-db6fdb0d8617',
 'c466d596-6779-43a3-ad09-575401f8b00a',
 '982b2d1f-6d6f-40d2-8656-f48021246384',
 '6e57e92f-ac4f-49fc-b9c2-4dd1ee9bccd7',
 'b11db9af-ea0f-45cd-93b7-663c135d9226']

# ==========================================
# 4. Define the Retrieval Tool for the Agent
# ==========================================
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information from the Machine Learning History document to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

# ==========================================
# 5. Initialize the LLM and the Agent
# ==========================================
llm = ChatOpenAI(
    model="nvidia/nemotron-3-nano-30b-a3b:free",
    temperature=0,
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

agent = create_agent(
    model=llm,
    tools=[retrieve_context],
    system_prompt=(
        "You are an expert AI historian and a helpful assistant. "
        "You have access to a tool that retrieves context from a document about Machine Learning History. "
        "Use the tool to search for answers. For multi-step questions, you must use the tool multiple times to gather all facts before answering."
    )
)

# ==========================================
# 6. Execution: Multi-Step Question
# ==========================================
print("🤖 Agent is thinking and searching...\n")
query = (
    "First, search to find out who coined the term 'machine learning' and in what year. "
    "Then, use a second search to find out who popularized the backpropagation algorithm later on."
)

result = agent.invoke({"messages": [HumanMessage(query)]})

print("✅ Final Agent Answer:")
print("="*50)
print(result["messages"][-1].content)
🤖 Agent is thinking and searching...

✅ Final Agent Answer:
==================================================
- **Coining of the term “machine learning”**: The phrase was introduced by **Arthur Samuel** in **1959** while he was working at IBM. He used it to describe a program that could improve its performance on a task (playing checkers) by learning from experience.

- **Popularization of the backpropagation algorithm**: The algorithm was brought into widespread use during the 1980s. It was popularized by **David Rumelhart, Geoffrey Hinton, and Ronald Williams** in **1986**, who demonstrated its power for training multi‑layer neural networks.
