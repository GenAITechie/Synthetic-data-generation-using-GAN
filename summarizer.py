# summarizer.py
import transformers
from transformers import BartForConditionalGeneration, BartTokenizer

def summarize(text, max_length=130, min_length=30):
    """
    Summarizes the input text using the BART model.

    Args:
        text (str): The text to be summarized.
        max_length (int): The maximum length of the summary.
        min_length (int): The minimum length of the summary.

    Returns:
        str: The summarized text.
    """
    # Load the pre-trained BART tokenizer and model
    model_name = 'facebook/bart-large-cnn'
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    # Encode the input text
    inputs = tokenizer.encode(
        text,
        return_tensors='pt',
        max_length=1024,
        truncation=True
    )

    # Generate a summary
    summary_ids = model.generate(
        inputs,
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # Decode and return the summary
    summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )
    return summary

if __name__ == "__main__":
    # Example usage
    print("Enter the text you want to summarize (press Enter twice to finish):\n")
    # Read multiline input from the user
    text_lines = []
    while True:
        line = input()
        if line:
            text_lines.append(line)
        else:
            break
    text = '\n'.join(text_lines)

    if text.strip():
        print("\nStarting summerization process..:\n")
        summary = summarize(text)
        print("\nSummary:\n")
        print(summary)
    else:
        print("No text was entered. Please run the script again and provide text to summarize.")