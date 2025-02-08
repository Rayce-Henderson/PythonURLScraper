import requests
from bs4 import BeautifulSoup

def scrape_and_parse_text(url):
    
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parses the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracts text content for Paragraphs under H1-H6
        paragraphs = soup.find_all('p')
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        extracted_text = []
        for heading in headings:
            extracted_text.append(heading.text.strip())  # Removes leading/trailing whitespace
        for paragraph in paragraphs:
            extracted_text.append(paragraph.text.strip())

        # Formats the extracted text for readability
        readable_text = "\n\n".join(extracted_text)

        return readable_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping or parsing: {e}")
        return None

# Saves the given text content to a text file.
def save_to_text_file(text_content, filename="scraped_data.txt"):
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text_content)
        print(f"Successfully saved scraped data to '{filename}'")
        return True
    except Exception as e:
        print(f"Error saving to file '{filename}': {e}")
        return False


if __name__ == "__main__":
    target_url = input("Enter the URL you want to scrape: ")
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    parsed_data = scrape_and_parse_text(target_url)

    if parsed_data:
        print("\n--- Scraped and Parsed Text ---")
        print(parsed_data)

        save_file_prompt = input("\nDo you want to save the scraped data to a text file? (yes/no): ").lower()
        if save_file_prompt == 'yes':
            filename = input("Enter the filename to save (e.g., my_data.txt): ") or "scraped_data.txt" # Default filename if user just presses Enter
            save_successful = save_to_text_file(parsed_data, filename)
            if not save_successful:
                print("Failed to save data to file.")
        else:
            print("Data not saved to file.")

    else:
        print("Failed to scrape and parse text from the URL.")
