import requests
import json
import time


# ==================================================
# CONFIGURATION
# ==================================================

API_URL = "http://127.0.0.1:8000/ask"


# ==================================================
# TEST DATASET
# ==================================================

test_cases = [

    {
        "question": "What is RAG?",
        "expected": [
            "retrieval-augmented generation",
            "retrieval augmented generation",
            "retrieve relevant information"
        ]
    },

    {
        "question": "Why is RAG useful?",
        "expected": [
            "external documents",
            "domain-specific information",
            "relevant information"
        ]
    },

    {
        "question": "What does an AI Engineer do?",
        "expected": [
            "artificial intelligence",
            "llms",
            "rag"
        ]
    },

    {
        "question": "What is Python?",
        "expected": [
            "programming language",
            "high-level programming language",
            "simple syntax"
        ]
    },

    {
        "question": "What is the capital of France?",
        "expected": [
            "i don't know",
            "don't know",
            "available documents"
        ]
    }

]


# ==================================================
# SEND QUESTION
# ==================================================

def ask_rag(question):

    start_time = time.time()

    response = requests.post(
        API_URL,
        json={
            "question": question
        },
        timeout=120
    )

    elapsed = time.time() - start_time

    return response, elapsed


# ==================================================
# EVALUATION
# ==================================================

results = []
passed = 0

print()
print("=" * 60)
print("RAG EVALUATION")
print("=" * 60)
print()


for index, test in enumerate(test_cases, start=1):

    question = test["question"]
    expected = test["expected"]

    print(
        f"[{index}/{len(test_cases)}] {question}"
    )

    try:

        response, latency = ask_rag(question)

        # ------------------------------------------
        # HTTP CHECK
        # ------------------------------------------

        if response.status_code != 200:

            print(
                f"❌ HTTP {response.status_code}"
            )

            results.append({
                "question": question,
                "expected": expected,
                "answer": "",
                "passed": False,
                "latency": latency
            })

            continue

        # ------------------------------------------
        # PARSE JSON RESPONSE
        # ------------------------------------------

        data = response.json()

        answer = data.get(
            "answer",
            ""
        )

        # ------------------------------------------
        # CHECK EXPECTED KEYWORDS
        # ------------------------------------------

        answer_lower = answer.lower()

        matched_keyword = None

        for keyword in expected:

            if keyword.lower() in answer_lower:

                matched_keyword = keyword
                break

        passed_test = matched_keyword is not None

        # ------------------------------------------
        # RESULT
        # ------------------------------------------

        if passed_test:

            passed += 1

            status = "✅ PASS"

        else:

            status = "❌ FAIL"

        print(
            f"{status} | Latency: {latency:.2f}s"
        )

        print(
            f"Answer: {answer[:200]}"
        )

        if matched_keyword:

            print(
                f"Matched: {matched_keyword}"
            )

        print()

        results.append({

            "question": question,

            "expected": expected,

            "answer": answer,

            "passed": passed_test,

            "matched_keyword": matched_keyword,

            "latency": latency

        })

    except Exception as e:

        print(
            f"❌ ERROR: {e}"
        )

        print()

        results.append({

            "question": question,

            "expected": expected,

            "answer": "",

            "passed": False,

            "matched_keyword": None,

            "latency": 0,

            "error": str(e)

        })


# ==================================================
# FINAL RESULTS
# ==================================================

total = len(test_cases)

accuracy = (
    passed / total
) * 100


print("=" * 60)
print("FINAL RESULTS")
print("=" * 60)

print(
    f"Passed: {passed}/{total}"
)

print(
    f"Accuracy: {accuracy:.2f}%"
)

print()


# ==================================================
# SAVE RESULTS
# ==================================================

with open(
    "evaluation_results.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(

        {
            "accuracy": accuracy,
            "passed": passed,
            "total": total,
            "results": results
        },

        file,

        indent=4,

        ensure_ascii=False
    )


print(
    "Results saved to evaluation_results.json"
)