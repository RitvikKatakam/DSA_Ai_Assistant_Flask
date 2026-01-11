# ===================== LIBRARIES =====================
from flask import Flask, render_template, request
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# History persistence disabled: conversations are not saved to disk.


# History helper functions removed — storing conversations is disabled by user request.

# ===================== LOAD ENV =====================
load_dotenv()
Grok = os.getenv("Grok_api_key")

# ===================== INITIALIZE FLASK =====================
app = Flask(__name__)

# History persistence is disabled (no DB is created)

# ===================== INITIALIZE GROQ =====================
llm = ChatGroq(
    temperature=0,
    groq_api_key=Grok,
    model="openai/gpt-oss-120b"
)


# ===================== ROUTES =====================

# ===================== PROMPT =====================
DSA_PROMPT = """
You are a DSA Preparation Assistant for coding interviews.

Guidelines:
- Explain concepts step by step
- Use simple language
- Give examples
- Mention time and space complexity
- Provide optimal approach
- If code is needed, use Python
- Ask one follow-up question at the end

Question:
{question}
"""

# ===================== FUNCTION =====================
def ask_dsa(question):
    prompt = DSA_PROMPT.format(question=question)
    response = llm.invoke(prompt)
    return response.content

# ===================== DSA TOPICS =====================
DSA_TOPICS = {
    "Arrays": [
        "Explain arrays with example",
        "Two Sum problem",
        "Kadane’s Algorithm"
    ],
    "Linked List": [
        "Singly vs Doubly Linked List",
        "Reverse a linked list",
        "Detect cycle in linked list"
    ],
    "Stack": [
        "Stack operations",
        "Valid Parentheses problem",
        "Next Greater Element"
    ],
    "Queue": [
        "Queue vs Deque",
        "Implement queue using stack",
        "Sliding Window Maximum"
    ],
    "Hashing": [
        "HashMap and HashSet",
        "Frequency counting",
        "Two Sum using hashing"
    ],
    "Recursion": [
        "Explain recursion with example",
        "Recursion vs Iteration",
        "Tower of Hanoi"
    ],
    "Binary Search": [
        "Binary Search algorithm",
        "Search in rotated array",
        "First and last occurrence"
    ],
    "Trees": [
        "Binary Tree vs BST",
        "Tree traversals",
        "Height of a binary tree"
    ],
    "Graphs": [
        "BFS vs DFS",
        "Detect cycle in graph",
        "Dijkstra’s algorithm"
    ],
    "Dynamic Programming": [
        "What is DP?",
        "0/1 Knapsack",
        "Longest Common Subsequence"
    ]
}

# ===================== ROUTES =====================
@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    question = ""

    if request.method == "POST":
        posted_question = request.form.get("question")
        if posted_question:
            answer = ask_dsa(posted_question)
            # clear the input after one question (do not pre-fill the textarea)
            question = ""
        else:
            question = ""

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        topics=DSA_TOPICS
    )

# ===================== RUN =====================
if __name__ == "__main__":
    app.run(debug=True)
