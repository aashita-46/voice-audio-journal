summarizer.py- from transformers import pipeline

summarizer = pipeline("text2text-generation", model="google/flan-t5-small")

def generate_summary(text):
    if len(text.strip()) < 50:
        return "Not enough content"

    result = summarizer(
        f"Summarize this: {text}",
        max_length=100,
        do_sample=False
    )
    return result[0]["generated_text"]