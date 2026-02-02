import os
from src.pipeline import DocumentPipeline
from research.neptune_monitor import NeptuneMonitor
from research.test_cases import TEST_PDFS, TEST_QUESTIONS


CHUNK_SIZES = [100, 200, 400, 800]


class ChunkExperiment:
    def __init__(self):
        self.monitor = NeptuneMonitor(experiment_name="chunk_size_experiment")

    def run(self):
        for chunk_size in CHUNK_SIZES:
            print(f"\n🧩 Testing chunk size: {chunk_size}")

            pipeline = DocumentPipeline()
            pipeline.chunker.fixed_chunk_size = chunk_size  # override adaptive chunking

            for pdf in TEST_PDFS:
                if not os.path.exists(pdf):
                    continue

                doc_info = pipeline.upload_document(pdf)

                for q in TEST_QUESTIONS:
                    answer, chunks, _ = pipeline.chat(q)

                    self.monitor.log_experiment_params({
                        "chunk_size_tested": chunk_size,
                        "file": os.path.basename(pdf),
                    })

                    self.monitor.log_question(
                        question=q,
                        answer=answer,
                        retrieved_chunks=chunks,
                        debug_info={"chunk_size": chunk_size}
                    )

        self.monitor.stop()


if __name__ == "__main__":
    ChunkExperiment().run()
