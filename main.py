from collections import Counter
from config import user_email, topic, RQs, short_name
from screening import *
from utils import *

if __name__ == "__main__":
    input_file_path = f'input/{short_name}.bib'
    papers = extract_papers(input_file_path)

    classifications = classify_papers(
        papers,
        strictness_level=10,
        study_topic=topic,
        research_questions=RQs
    )

    for i in range(len(classifications)):
        print(f"{i}: {classifications[i]}")
    print()

    count = Counter(classifications)

    for value in range(5):
        print(f"{value}: {count[value]}")

    selected_papers = []
    for idx, paper in enumerate(papers):
        if classifications[idx] > 3:
            print("Processing paper:", paper["title"])
            pdf_url = get_pdf_url(paper["doi"], user_email)

            if pdf_url:
                try:
                    print(f"\tPDF available at: {pdf_url}")
                    download_pdf(pdf_url, "temp_paper.pdf")
                    full_text = extract_text_from_pdf("temp_paper.pdf")
                    summary, classification = summarize_full_text(full_text=full_text, study_topic=topic, research_questions=RQs)
                    # print(summary, classification, sep="\n\n")
                    if(classification >= 3):
                        selected_papers.append(paper)
                        write_summary_to_file(summary, f"output/{short_name}/{idx}.txt")
                except:
                    print("Couldn't access the found PDF file.")
            else:
                print("\tNo open access PDF found.")

    save_papers_to_bibtex(selected_papers, f"output/{short_name}.bib")


