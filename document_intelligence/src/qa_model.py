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




from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class QAModel:
    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1

        # -------------------------------
        # Extractive QA (FACTUAL)
        # -------------------------------
        print("⚡ Loading Extractive QA model (DistilBERT)...")
        self.extractive_qa = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad",
            device=device
        )

        # -------------------------------
        # Generative QA (CONCEPTUAL)
        # -------------------------------
        print("🤖 Loading Generative QA model (Flan-T5)...")
        self.gen_tokenizer = AutoTokenizer.from_pretrained(
            "google/flan-t5-small"
        )
        self.gen_model = AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-small"
        ).to("cuda" if torch.cuda.is_available() else "cpu")

        print("✅ Hybrid QA Models Loaded")

    # -------- Extractive --------
    def extract_answer(self, context, question):
        try:
            result = self.extractive_qa(
                question=question,
                context=context[:2000]
            )
            return result.get("answer", "").strip()
        except Exception:
            return ""

    # -------- Generative --------
    def generate_answer(self, context, question):
        prompt = f"""
Answer the question using ONLY the document below.

Document:
{context}

Question:
{question}
"""

        inputs = self.gen_tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.gen_model.device)

        outputs = self.gen_model.generate(
            **inputs,
            max_new_tokens=150
        )

        return self.gen_tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        ).strip()
