import json
from datetime import datetime


def generate_report():
    report = {
        "project": "RAG Evaluation Report",
        "generated_at": str(datetime.now()),
        "summary": {
            "note": "Check Neptune AI dashboard for detailed visual analysis."
        }
    }

    with open("rag_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("📊 RAG report generated: rag_report.json")


if __name__ == "__main__":
    generate_report()
