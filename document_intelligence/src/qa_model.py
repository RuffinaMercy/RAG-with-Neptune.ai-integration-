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








from transformers import pipeline
import torch


class QAModel:
    def __init__(self):
        print("⚡ Loading Extractive QA model (Colab-safe mode)")

        device_id = 0 if torch.cuda.is_available() else -1

        self.extractive_qa = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad",
            device=device_id
        )

    def extract_answer(self, context, question):
        try:
            result = self.extractive_qa(
                question=question,
                context=context[:2000]
            )
            return result.get("answer", "")
        except:
            return ""

    def generate_answer(self, context, question):
        return "⚠️ Generative model disabled in Colab"
