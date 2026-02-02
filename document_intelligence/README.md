
---

# 📚 Document Intelligence RAG System

## 🧠 Overview

This project is an advanced **Document Intelligence System** built using **Retrieval-Augmented Generation (RAG)**.
It enables users to upload documents (PDF/TXT/DOCX), interact with them using a chatbot, highlight keywords in PDFs, and evaluate RAG performance through automated experiments.

The system integrates:

* ⚡ Hybrid RAG (Extractive + Generative Models)
* 🧩 Adaptive Chunking
* 🔍 Semantic Retrieval using Embeddings
* 🤖 Question Answering (DistilBERT + Phi-3)
* 🌐 Streamlit UI
* 📊 Research & Evaluation Framework
* 🌊 Neptune.ai Experiment Tracking
* 📈 Excel-based Experiment Reports

This project is designed both as a **production-ready RAG application** and a **research framework** for evaluating RAG systems.

---

## 🚀 Features

### 1️⃣ Document Chat (RAG-based)

* Upload PDF / TXT / DOCX files
* Ask questions about the document
* Hybrid QA system:

  * Extractive model: DistilBERT
  * Generative model: Phi-3
* Context-aware answers using retrieved chunks

---

### 2️⃣ Adaptive Chunking

* Automatically determines chunk size based on document length
* Prevents chunk explosion using hard limits
* Optimized for:

  * Small documents
  * Medium documents
  * Large documents

---

### 3️⃣ Semantic Retrieval

* Sentence Transformers (`all-MiniLM-L6-v2`)
* Cosine similarity-based chunk retrieval
* Top-k relevant chunk selection

---

### 4️⃣ PDF Keyword Highlighting

* Highlight user-defined keywords in PDFs
* Shows:

  * Found keywords
  * Missing keywords
* Generates highlighted PDF output

---

### 5️⃣ Streamlit User Interface

* Document upload panel
* Chatbot interface
* PDF viewer with highlights
* Keyword highlighting panel

---

### 6️⃣ Research & Evaluation Framework

Located in the `research/` folder.

Supports:

* Multiple documents testing
* Multiple prompts per document
* Multiple questions per document
* Automated RAG evaluation
* Model comparison
* Chunking experiments
* Prompt experiments

---

### 7️⃣ Neptune.ai Integration

* Logs experiments in real-time
* Tracks:

  * Questions
  * Answers
  * Retrieved chunks
  * Response time
  * Model used
  * Document metadata
* Visual dashboards for RAG analysis

---

### 8️⃣ Excel Experiment Report

* Automatically generated after experiments
* Contains:

  * Document name
  * Prompt
  * Question
  * Answer
  * Chunks used
  * Chunk size
  * Response time
  * Model used

---

## 🏗️ Project Architecture

```
document_intelligence/
│
├── app.py                     # Streamlit UI
├── config.py                  # Configuration settings
├── requirements.txt
├── README.md
│
├── src/                       # Core RAG pipeline
│   ├── pipeline.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── qa_model.py
│   ├── adaptive_chunker.py
│   ├── document_loader.py
│   ├── pdf_highlighter.py
│
├── research/                  # RAG evaluation framework
│   ├── test_cases.py
│   ├── experiment_runner.py
│   ├── neptune_monitor.py
│   ├── model_comparison.py
│   ├── chunk_experiments.py
│   ├── prompt_experiments.py
│   ├── report_generator.py
│
├── data/                      # Uploaded documents
├── highlighted_pdfs/          # Output PDFs
├── temp_images/
└── rag_test_results.xlsx      # Experiment results
```

---

## 🧠 Hybrid RAG Pipeline Flow

### 🟢 Application Mode (Streamlit)

```
Document Upload
      ↓
Text Extraction
      ↓
Adaptive Chunking
      ↓
Embeddings Generation
      ↓
Semantic Retrieval
      ↓
Hybrid QA Models
(DistilBERT + Phi-3)
      ↓
Answer Generation
      ↓
PDF Highlighting + Chat UI
```

---

### 🔵 Research Mode (Experiment Runner)

```
Multiple Documents
      ↓
Automated Test Cases
      ↓
Adaptive Chunking + Retrieval
      ↓
Hybrid QA Models
      ↓
Neptune Logging
      ↓
Excel Report Generation
```

---

## 🤖 Models Used

### 🔹 Embedding Model

* `sentence-transformers/all-MiniLM-L6-v2`

### 🔹 Extractive QA Model

* `distilbert-base-cased-distilled-squad`

### 🔹 Generative LLM

* `microsoft/phi-3-mini-4k-instruct`

---

## 🛠️ Technologies & Platforms

| Category            | Tools                    |
| ------------------- | ------------------------ |
| Language            | Python                   |
| UI                  | Streamlit                |
| NLP Models          | HuggingFace Transformers |
| Embeddings          | Sentence Transformers    |
| PDF Processing      | PyMuPDF (fitz)           |
| Experiment Tracking | Neptune.ai               |
| Data Analysis       | Pandas, Excel            |
| ML Ops              | Hybrid RAG Pipeline      |
| GPU Support         | PyTorch + CUDA           |

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone <repo-url>
cd document_intelligence
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Streamlit App

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🧪 Run RAG Experiments

```bash
python research/experiment_runner.py
```

---

## 🌊 Enable Neptune.ai

Set environment variables:

```powershell
setx NEPTUNE_PROJECT "your-workspace/your-project"
setx NEPTUNE_API_TOKEN "your-api-token"
```

Restart terminal and run experiments again.

---

## 📊 Output Files

* `rag_test_results.xlsx` → Experiment results
* Neptune Dashboard → Visual RAG analysis
* Highlighted PDFs → Keyword visualization

---

## 🔬 Research Capabilities

This system supports:

* Multi-document RAG testing
* Prompt engineering experiments
* Chunk size analysis
* Model comparison (Extractive vs Generative)
* Performance benchmarking
* RAG reliability testing
* Negative question testing (hallucination detection)

---

## 💡 Key Insights from the Project

* Hybrid RAG improves accuracy and speed
* Adaptive chunking must be constrained
* Extractive models are faster for factual queries
* Generative models are better for reasoning
* Experiment tracking is essential for RAG evaluation

---

## 🎯 Use Cases

* Document Q&A Systems
* Resume Analysis
* Academic Document Understanding
* Legal / Policy Document Search
* Research Paper Analysis
* Enterprise Knowledge Assistants
* RAG Benchmarking Framework

---

## 🧑‍💻 Author

**Ruffina Mercy S**
Aspiring AI Engineer & Data Scientist
Project: Document Intelligence RAG System

---

