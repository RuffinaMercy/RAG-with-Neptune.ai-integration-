import sys
import os
import time
import pandas as pd

# ✅ Fix Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.pipeline import DocumentPipeline
from research.neptune_monitor import NeptuneMonitor
from research.test_cases import DOCUMENT_TEST_CASES, TEST_PDFS


class RAGExperimentRunner:
    def __init__(self):
        self.pipeline = DocumentPipeline()
        self.monitor = NeptuneMonitor(experiment_name="rag_document_wise_testing")

        # Store results for Excel
        self.results = []

    def run(self):
        for pdf_path in TEST_PDFS:
            if not os.path.exists(pdf_path):
                print(f"❌ File not found: {pdf_path}")
                continue

            file_name = os.path.basename(pdf_path)
            print(f"\n📂 Testing Document: {file_name}")

            # Load document
            doc_info = self.pipeline.upload_document(pdf_path)

            # Log metadata to Neptune
            self.monitor.log_experiment_params({
                "document_name": file_name,
                "file_size": os.path.getsize(pdf_path),
                "chunk_size": doc_info["chunk_size"],
                "chunks_count": doc_info["chunks"],
            })

            if file_name not in DOCUMENT_TEST_CASES:
                print(f"⚠️ No test cases for {file_name}")
                continue

            test_config = DOCUMENT_TEST_CASES[file_name]
            questions = test_config["questions"]
            prompts = test_config["prompts"]

            for prompt in prompts:
                for q in questions:
                    final_question = f"{prompt} {q}"

                    start_time = time.time()
                    answer, chunks, debug_info = self.pipeline.chat(final_question)
                    response_time = round(time.time() - start_time, 3)

                    debug_info = debug_info or {}

                    # Save result for Excel
                    self.results.append({
                        "Document": file_name,
                        "Prompt": prompt,
                        "Question": q,
                        "Final Question": final_question,
                        "Answer": answer,
                        "Chunks Used": len(chunks),
                        "Chunk Size": doc_info["chunk_size"],
                        "Response Time (s)": response_time,
                        "Model Used": debug_info.get("model", "unknown"),
                    })

                    # Log to Neptune
                    self.monitor.log_question(
                        question=final_question,
                        answer=answer,
                        retrieved_chunks=chunks,
                        debug_info={
                            "document": file_name,
                            "prompt": prompt,
                            "response_time": response_time,
                            "chunks_used": len(chunks),
                            "model": debug_info.get("model", "unknown"),
                        }
                    )

                    print(f"🧪 Q: {final_question}")
                    print(f"🤖 A: {answer}")
                    print("-" * 60)

        self.monitor.stop()
        self.save_excel()

    def save_excel(self):
        if not self.results:
            print("⚠️ No results to save.")
            return

        df = pd.DataFrame(self.results)
        output_path = "rag_test_results.xlsx"
        df.to_excel(output_path, index=False)

        print(f"\n📊 Excel Report Generated: {output_path}")


if __name__ == "__main__":
    runner = RAGExperimentRunner()
    runner.run()
