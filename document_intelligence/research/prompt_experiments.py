from src.pipeline import DocumentPipeline
from research.neptune_monitor import NeptuneMonitor
from research.test_cases import TEST_PDFS, TEST_QUESTIONS, PROMPTS


class PromptExperiment:
    def __init__(self):
        self.pipeline = DocumentPipeline()
        self.monitor = NeptuneMonitor(experiment_name="prompt_experiment")

    def run(self):
        for pdf in TEST_PDFS:
            self.pipeline.upload_document(pdf)

            for prompt in PROMPTS:
                for q in TEST_QUESTIONS:
                    modified_question = f"{prompt} {q}"

                    answer, chunks, _ = self.pipeline.chat(modified_question)

                    self.monitor.log_question(
                        question=modified_question,
                        answer=answer,
                        retrieved_chunks=chunks,
                        debug_info={"prompt": prompt}
                    )

        self.monitor.stop()


if __name__ == "__main__":
    PromptExperiment().run()
