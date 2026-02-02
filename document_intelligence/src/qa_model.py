# from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
# import torch


# class QAModel:
#     def __init__(self, model_name=None, model_path=None):
#         print("⚡ Loading Extractive QA model (DistilBERT)...")

#         device = 0 if torch.cuda.is_available() else -1

#         # Extractive QA model (FAST)
#         self.extractive_qa = pipeline(
#             "question-answering",
#             model="distilbert-base-cased-distilled-squad",
#             device=device
#         )

#         print("🤖 Loading Generative Model (Phi-3)...")

#         self.gen_tokenizer = AutoTokenizer.from_pretrained(
#             model_path,
#             trust_remote_code=True
#         )

#         self.gen_model = AutoModelForCausalLM.from_pretrained(
#             model_path,
#             trust_remote_code=True,
#             torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
#             device_map="auto"
#         )

#         print("✅ Hybrid QA Models Loaded")

#     # ================= EXTRACTIVE ANSWER ================= #
#     def extract_answer(self, context, question):
#         try:
#             result = self.extractive_qa(
#                 question=question,
#                 context=context[:2000]
#             )
#             return result["answer"]
#         except:
#             return ""

#     # ================= GENERATIVE ANSWER ================= #
#     def generate_answer(self, context, question):
#         prompt = f"""
# You are an AI assistant. Answer ONLY using the given document.

# Document:
# {context}

# Question:
# {question}

# Answer:
# """

#         inputs = self.gen_tokenizer(prompt, return_tensors="pt").to(self.gen_model.device)

#         outputs = self.gen_model.generate(
#             **inputs,
#             max_new_tokens=120,
#             temperature=0.3,
#             do_sample=True
#         )

#         answer = self.gen_tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return answer.split("Answer:")[-1].strip()










from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch


class QAModel:
    def __init__(self, model_name="microsoft/phi-3-mini-4k-instruct"):
        """
        Hybrid QA Model:
        - Extractive QA: DistilBERT (fast, factual)
        - Generative QA: Phi-3 (reasoning + fallback)
        """

        # -------------------------------
        # Device selection
        # -------------------------------
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        device_id = 0 if self.device == "cuda" else -1

        print("⚡ Loading Extractive QA model (DistilBERT)...")

        # -------------------------------
        # Extractive QA (FAST)
        # -------------------------------
        self.extractive_qa = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad",
            device=device_id
        )

        print("🤖 Loading Generative Model (Phi-3)...")

        # -------------------------------
        # Generative QA (Phi-3)
        # -------------------------------
        self.gen_tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        self.gen_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map="auto",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )

        print("✅ Hybrid QA Models Loaded Successfully")

    # ======================================================
    # Extractive Answer (first attempt)
    # ======================================================
    def extract_answer(self, context, question):
        try:
            result = self.extractive_qa(
                question=question,
                context=context[:2000]  # safety limit
            )
            return result.get("answer", "").strip()
        except Exception:
            return ""

    # ======================================================
    # Generative Answer (fallback / reasoning)
    # ======================================================
    def generate_answer(self, context, question):
        prompt = f"""
You are a document-based AI assistant.
Answer ONLY using the given document content.
If the answer is not present, say:
"⚠️ Answer not found in the document."

Document:
{context}

Question:
{question}

Answer:
"""

        inputs = self.gen_tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=4096
        ).to(self.gen_model.device)

        with torch.no_grad():
            outputs = self.gen_model.generate(
                **inputs,
                max_new_tokens=120,
                temperature=0.3,
                do_sample=True
            )

        decoded = self.gen_tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return decoded.split("Answer:")[-1].strip()
