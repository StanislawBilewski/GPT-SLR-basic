# Systematic Literature Review Assistant

This project is a Systematic Literature Review (SLR) Assistant designed to help researchers conduct comprehensive and systematic reviews of academic literature. The app leverages GPT-4 for various tasks in the SLR process, such as title and abstract screening, full-text review, and keyword generation.

## Features

- **Title and Abstract Screening**: Screen titles and abstracts for relevance using GPT-4, classifying papers into different levels of usefulness.
- **Full-Text Review**: Extract key information from full-text PDFs and summarize content for easier analysis.
- **PDF Handling**: Automatically download and process open-access PDFs for full-text analysis.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- [OpenAI API Key](https://platform.openai.com/signup) (You must have access to GPT-4)

### Libraries

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

### .env Setup

Create a `.env` file in the root directory of the project with the following content:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
USER_EMAIL=your_email_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key and `your_email_here` with your actual e-mail address.

## Usage

### Config

Before you start your first study in GPT-SLR, you'll have to edit the contents of the `config.py` file.
The lines that need to be edited are:
```python
topic="Age-Related Macular Degeneration - mechanism, symptoms, treatment"
RQs="""
    1. What are the mechanisms and pathophysiological processes involved in the development and progression of age-related macular degeneration (AMD)?
    2. What are the clinical symptoms of age-related macular degeneration, and what diagnostic methods are most effective in detecting and staging the disease?
    3. What are the current treatment options for both dry and wet forms of age-related macular degeneration, and how can these treatments be optimized for better efficacy and patient outcomes?
"""
short_name = "AMD"
```
The `topic` variable represents the study topic.
The `RQs` variable represents your study's research questions
The `short_name` variable is used to access the input files and to store output files.
The references to be imported should be placed in the `input/<short_name>.bib` file in the bibtex format.
The final selection of papers will be stored in the `output/<short_name>.bib` file, and the full-text summaries in the `ouput/<short_name>/` directory.

You can also chose to use a different GPT model, especially if you would like to not limit your expenses. See [here](https://openai.com/api/pricing/).

### Title and Abstract Screening + Full-text Review and final paper selection

The main.py script runs basic title&abstract screening, classifying the imported references into 5 classes:
* Perfect fit for the research
* Definitely useful
* Might be useful
* Probably not useful
* Completely unrelated

The papers that reached a high enough classification are then reviewed in full-text, assuming the paper is open-access. Currently, version of GPT-SLR does not have the option of importing your own pdf files for the papers, instead it downloads them automatically via Unpaywall API - but only the ones that have a public, legal and free source for the pdf file. The ones that are not open-access are ignored and not taken into consideration. *This limitation will most likely be addressed in the future.*

### Notes

- The app currently supports basic functionality and may require further development for more advanced features and ease of access.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

Please note that accessing copyrighted material through unauthorized means (such as Sci-Hub) is illegal and unethical. This project strictly adheres to legal and ethical guidelines for accessing academic papers.