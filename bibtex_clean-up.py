import re

from config import short_name

def remove_non_ascii(text):
    # Remove non-ASCII characters using regular expression
    return re.sub(r'[^\x00-\x7F]+', '', text)

def clean_bibtex_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove non-ASCII characters
    cleaned_content = remove_non_ascii(content)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

if __name__ == "__main__":
    input_file = f'input/{short_name}_org.bib'
    output_file = f'input/{short_name}.bib'

    clean_bibtex_file(input_file, output_file)
    print(f"Cleaned BibTeX file has been saved to {output_file}")
