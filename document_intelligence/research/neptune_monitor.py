import os
from datetime import datetime
import neptune


class NeptuneMonitor:
    def __init__(self, experiment_name="rag_experiment"):
        project = os.getenv("NEPTUNE_PROJECT")
        api_token = os.getenv("NEPTUNE_API_TOKEN")

        if not project or not api_token:
            print("⚠️ Neptune Disabled (API token or project not found in environment)")
            self.enabled = False
            self.run = None
            return

        print("🌊 Neptune Enabled")
        self.enabled = True

        self.run = neptune.init_run(
            project=project,
            api_token=api_token,
            name=experiment_name,
        )

        self.run["system/experiment_name"] = experiment_name
        self.run["system/start_time"] = str(datetime.now())

    def log_experiment_params(self, params: dict):
        if not self.enabled:
            return
        for k, v in params.items():
            self.run[f"experiment/{k}"] = v

    def log_question(self, question, answer, retrieved_chunks, debug_info=None):
        if not self.enabled:
            return {}

        entry = {
            "timestamp": str(datetime.now()),
            "question": question,
            "answer": answer,
            "chunks_count": len(retrieved_chunks),
            "debug_info": debug_info or {},
        }

        self.run["history"].append(entry)
        return entry

    def stop(self):
        if self.enabled:
            self.run["system/end_time"] = str(datetime.now())
            self.run.stop()
            print("🛑 Neptune Run Stopped")
