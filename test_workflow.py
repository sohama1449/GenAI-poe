
print("Medical Healthcare AI Test Started!")

from workflow import get_medical_response

question = "What are some common causes of headaches?"

result = get_medical_response(question)

print("\n========== RESULTS ==========")
print("Question:", result["question"])
print("Category:", result["category"])
print("\nFinal Medical Response:")
print(result["final_response"])
print("\n========== TEST COMPLETED ==========")
