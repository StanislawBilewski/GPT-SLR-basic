import openai

from config import openai_model

client = openai.OpenAI()

def classify_papers(papers, strictness_level, study_topic, research_questions):
    # Initialize the conversation with the system prompt
    system_prompt = f"""
            You are an expert in Systematic Literature Search. The topic of the studies is: {study_topic}, with these research questions:
            {research_questions}

            Based on the received titles and abstracts, classify each paper's usefulness.
            The level of strictness when judging the papers is: {strictness_level}/10.
            For the maximum strictness level be EXTREMELY selective when judging the papers.
            The allowed classifications are:
            - 4 (Perfect fit for the research)
            - 3 (Definitely useful)
            - 2 (Might be useful)
            - 1 (Probably not useful)
            - 0 (Completely unrelated)
            Answer only in one number - the chosen classification, nothing more.
        """

    classifications = []

    for i, paper in enumerate(papers):
        title, abstract = paper['title'], paper['abstract']
        
        # Create the user message
        user_message = f"Title: {title}\nAbstract: {abstract}\nClassify this paper's usefulness."
        
        # Call GPT API with the current conversation
        response = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ]
        )
        
        # Extract the classification
        classification = response.choices[0].message.content.strip()
        try:
            classifications.append(int(classification))
        except:
            print("Improper classification! Returned a non-int value!")

    return classifications

def summarize_full_text(full_text, study_topic, research_questions):

    # System prompt for GPT
    system_prompt = f"""
    You are an expert in Systematic Literature Search. The topic of the studies is: {study_topic}, with the following research questions:
            {research_questions}
    Your task is to extract key data points (e.g., study objectives, methodologies, results) from the provided full-text paper.
    Then, provide a concise summary to facilitate a quick understanding of the content.
    """

    # Call GPT API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_text},
            ]
        )
    
    # Extract the summary
    summary = response.choices[0].message.content.strip()
    
    prompt = """Could you now classify whether this paper based on the reviewed full text?
            The allowed classifications are:
            - 4 (Perfect fit for the research)
            - 3 (Definitely useful)
            - 2 (Might be useful)
            - 1 (Probably not useful)
            - 0 (Completely unrelated)
            Answer only in one number - the chosen classification, nothing more.
        """
    
    response = client.chat.completions.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_text},
            {"role": "assistant", "content": summary},
            {"role": "user", "content": prompt}
            ]
        )
    
    try:
        classification = int(response.choices[0].message.content.strip())
    except:
        print("Improper classification! Returned a non-int value!")
        classification = 0

    return summary, classification