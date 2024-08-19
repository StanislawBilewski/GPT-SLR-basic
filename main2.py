import openai
import os
import openai
import bibtexparser

from collections import Counter
from dotenv import load_dotenv

def extract_titles_and_abstracts(bibtex_file_path):
    with open(bibtex_file_path) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    papers = []
    for entry in bib_database.entries:
        title = entry.get('title', 'No title available').strip('{}')
        abstract = entry.get('abstract', None)
        papers.append({'title': title, 'abstract': abstract})
    
    return papers

client = openai.OpenAI()

def classify_papers(papers, strictness_level, study_topic):
    # Initialize the conversation with the system prompt
    messages = [
        {"role": "system", "content": f"""
            You are an expert in Systematic Literature Search. The topic of the studies is: {study_topic}, with these research questions:
            1. What are the key differences between 3rd generation neural networks and previous generations?
            2. How do 2nd-gen and 3rd-gen neural networks differ in terms of energy consumption and accuracy on standard benchmarks?
            3. What are the differences in training complexity and scalability between 2nd-gen and 3rd-gen neural networks?
            4. How do 2nd-gen and 3rd-gen neural networks compare in robustness to adversarial attacks?

            Based on the received titles and abstracts, classify each paper's usefulness.
            The level of strictness when judging the papers is: {strictness_level}/10.
            The allowed classifications are:
            - 4 (Perfect fit for the research)
            - 3 (Definitely useful)
            - 2 (Might be useful)
            - 1 (Probably not useful)
            - 0 (Completely unrelated)
            Answer only in one number - the chosen classification, nothing more.
        """}
    ]

    classifications = []

    for i, paper in enumerate(papers):
        title, abstract = paper['title'], paper['abstract']
        
        # Create the user message
        user_message = {"role": "user", "content": f"Title: {title}\nAbstract: {abstract}\nClassify this paper's usefulness."}
        
        # Add the user message to the conversation
        messages.append(user_message)
        
        # Call GPT API with the current conversation
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        # Extract the classification
        classification = response.choices[0].message.content.strip()
        try:
            classifications.append(int(classification))
        except:
            print("Improper classification! Returned a non-int value!")
        
        # Append the assistant's response to continue the conversation context
        messages.append({"role": "assistant", "content": classification})

    return classifications

def summarize_full_text(full_text, study_topic):

    # System prompt for GPT
    system_prompt = f"""
    You are an expert in Systematic Literature Search. The topic of the studies is: {study_topic}.
    Your task is to extract key data points (e.g., study objectives, methodologies, results) from the provided full-text paper.
    Then, provide a concise summary to facilitate a quick understanding of the content.
    """

    # GPT prompt
    prompt = f"Full-text paper:\n{full_text}\nPlease extract key points and summarize."

    # Call GPT API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
            ]
        )
    
    # Extract the summary
    summary = response.choices[0].message.content.strip()

    return summary

if __name__ == "__main__":
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Set the API key for OpenAI
    openai.api_key = openai_api_key
    
    bibtex_file_path = 'bibtex/SNNvsANN.bib'
    papers = extract_titles_and_abstracts(bibtex_file_path)[30:40]

    classifications = classify_papers(papers, strictness_level=10, study_topic="Comparative analysis of second and third generation neural networks")
    for i in range(len(classifications)):
        print(f"{i}: {classifications[i]}")
    print()

    count = Counter(classifications)

    # Print the summary
    for value in range(5):
        print(f"{value}: {count[value]}")



    # full_text = """... (Full paper text) ..."""
    # summary = summarize_full_text(full_text, study_topic="AI in Healthcare")
    # print(summary)
