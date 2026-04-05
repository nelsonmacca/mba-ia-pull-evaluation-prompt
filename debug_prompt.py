import json
from langchain import hub
from dotenv import load_dotenv
from src.utils import get_llm

load_dotenv()

prompt = hub.pull("bug_to_user_story_v2")
llm = get_llm(temperature=0)
chain = prompt | llm

with open("datasets/bug_to_user_story.jsonl", "r", encoding="utf-8") as f:
    lines = [json.loads(line) for line in f if line.strip()]

for i, item in enumerate(lines[:10], 1):
    bug_report = item["inputs"]["bug_report"]
    reference = item["outputs"]["reference"]

    response = chain.invoke({"bug_report": bug_report})
    answer = response.content

    print("=" * 100)
    print(f"EXEMPLO {i}")
    print("=" * 100)
    print("\nBUG REPORT:\n")
    print(bug_report)
    print("\nRESPOSTA GERADA:\n")
    print(answer)
    print("\nREFERÊNCIA:\n")
    print(reference)
    print("\n")