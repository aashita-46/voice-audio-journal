from transformers import pipeline

print("Loading summarization model...")

# flan-t5 is a text2text model, must use "text2text-generation" pipeline
summarizer = pipeline("text2text-generation", model="google/flan-t5-base")


def generate_summary(text):
    if len(text.strip()) < 50:
        return "Not enough content to summarize."

    try:
        prompt = f"Summarize this journal entry and reflect on the mood:\n{text}"

        result = summarizer(
            prompt,
            max_length=150,
            do_sample=False
        )

        return result[0]['generated_text'].strip()

    except Exception as e:
        return f"Error generating summary: {e}"