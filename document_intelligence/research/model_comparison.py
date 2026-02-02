import os
from src.pipeline import DocumentPipeline
from research.neptune_monitor import NeptuneMonitor
from research.test_cases import TEST_PDFS, TEST_QUESTIONS


class ModelComparison:
    def __init__(self):
        self.pipeline = DocumentPipeline()
        self.monitor = NeptuneMonitor(experiment_name="model_comparison")

    def run(self):
        for pdf in TEST_PDFS:
            if not os.path.exists(pdf):
                continue

            print(f"\n🤖 Model comparison on: {pdf}")
            self.pipeline.upload_document(pdf)

            for q in TEST_QUESTIONS:
                ext_ans, gen_ans, chunks = self.pipeline.compare_models(q)

                self.monitor.log_model_comparison(
                    question=q,
                    model_a="DistilBERT",
                    ans_a=ext_ans,
                    model_b="Phi-3",
                    ans_b=gen_ans
                )

        self.monitor.stop()


if __name__ == "__main__":
    ModelComparison().run()
