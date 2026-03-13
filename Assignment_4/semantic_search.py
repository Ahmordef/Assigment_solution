!pip install -q langchain-community langchain-huggingface sentence-transformers

import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# ==========================================
# 0. Create a Custom Document (Risk Management Policy)
# ==========================================
doc_content = """
Najran University - Risk Management and Business Continuity Policy

1. Introduction
This document outlines the governance and risk management framework. The goal is to ensure business continuity during unforeseen disruptions.

2. Governance and Compliance
All departments must adhere to the central risk register. The Assistant Head of Department is responsible for quarterly risk audits and ensuring that the Liferay CMS is updated with the latest compliance protocols.

3. Power Outage Protocol
In the event of a critical power outage in the main server room, backup generators must be activated within 15 minutes. The IT Operations team will broadcast an emergency SMS to all staff.

4. Data Security
All sensitive university data must be backed up daily to off-site cloud servers.
"""

# حفظ النص في ملف
with open("risk_policy.txt", "w", encoding="utf-8") as f:
    f.write(doc_content)

# ==========================================
# 1. Load: قراءة المستند
# ==========================================
loader = TextLoader("risk_policy.txt")
docs = loader.load()
print("✅ Step 1 (Load): Document loaded successfully.")
✅ Step 1 (Load): Document loaded successfully.

# ==========================================
# 2. Split: تقسيم المستند إلى أجزاء
# ==========================================
text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
all_splits = text_splitter.split_documents(docs)
print(f"✅ Step 2 (Split): Document split into {len(all_splits)} chunks.")
✅ Step 2 (Split): Document split into 8 chunks.

# ==========================================
# 3. Embed: تحويل النصوص إلى متجهات
# ==========================================
print("⏳ Downloading embedding model... (this takes a moment)")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
print("✅ Step 3 (Embed): Embedding model loaded.")
 ⏳ Downloading embedding model... (this takes a moment)
/usr/local/lib/python3.12/dist-packages/huggingface_hub/utils/_auth.py:94: UserWarning: 
The secret `HF_TOKEN` does not exist in your Colab secrets.
To authenticate with the Hugging Face Hub, create a token in your settings tab (https://huggingface.co/settings/tokens), set it as secret in your Google Colab and restart your session.
You will be able to reuse this secret in all of your notebooks.
Please note that authentication is recommended but still optional to access public models or datasets.
  warnings.warn(
modules.json: 100% 349/349 [00:00<00:00, 24.1kB/s]config_sentence_transformers.json: 100% 116/116 [00:00<00:00, 8.78kB/s]README.md:  11.6k/? [00:00<00:00, 595kB/s]sentence_bert_config.json: 100% 53.0/53.0 [00:00<00:00, 3.15kB/s]config.json: 100% 571/571 [00:00<00:00, 24.8kB/s]model.safetensors: 100% 438M/438M [00:05<00:00, 83.9MB/s]Loading weights: 100% 199/199 [00:00<00:00, 451.31it/s, Materializing param=pooler.dense.weight]MPNetModel LOAD REPORT from: sentence-transformers/all-mpnet-base-v2
Key                     | Status     |  | 
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
tokenizer_config.json: 100% 363/363 [00:00<00:00, 18.0kB/s]vocab.txt:  232k/? [00:00<00:00, 5.09MB/s]tokenizer.json:  466k/? [00:00<00:00, 12.5MB/s]special_tokens_map.json: 100% 239/239 [00:00<00:00, 20.2kB/s]Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
WARNING:huggingface_hub.utils._http:Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
config.json: 100% 190/190 [00:00<00:00, 16.0kB/s]✅ Step 3 (Embed): Embedding model loaded.

# ==========================================
# 4. Store: تخزين المتجهات في قاعدة البيانات
# ==========================================
vector_store = InMemoryVectorStore(embeddings)
ids = vector_store.add_documents(documents=all_splits)
print("✅ Step 4 (Store): Chunks stored in InMemoryVectorStore.")
✅ Step 4 (Store): Chunks stored in InMemoryVectorStore.

  # ==========================================
# 5. Retrieve: البحث الدلالي والاسترجاع
# ==========================================
query = "What are the responsibilities of the Assistant Head of Department?"
print(f"\n🔍 Searching for: '{query}'\n")
🔍 Searching for: 'What are the responsibilities of the Assistant Head of Department?'

# إنشاء أداة الاسترجاع كما في الدرس
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 1})
results = retriever.invoke(query)

print("="*50)
print("🎯 Top Semantic Match Found:")
print(results[0].page_content)
print("="*50)
==================================================
🎯 Top Semantic Match Found:
All departments must adhere to the central risk register. The Assistant Head of Department is responsible for quarterly risk audits and ensuring that the Liferay CMS is updated with the latest
==================================================


