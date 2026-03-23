from transformers import pipeline

print("Loading summarization model...")

summarizer = pipeline("text-generation", model="google/flan-t5-base")

def generate_summary(text):
    if len(text.strip()) < 50:
        return "Not enough content to analyze yet."

    try:
        prompt = f"""
Summarize this journal entry:
{text}
"""

        result = summarizer(
            prompt,
            max_length=150,
            do_sample=False
        )

        output = result[0]['generated_text']
        return output.replace(prompt, "").strip()

    except Exception as e:
        return f"Error: {e}"