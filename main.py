import requests
from bs4 import BeautifulSoup

def scrape_and_parse_text(url):
    """
    Scrapes text data from a given URL and parses it into a readable format.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        str: Parsed and readable text content from the webpage, or None if scraping fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        paragraphs = soup.find_all('p')
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        extracted_text = []
        for heading in headings:
            extracted_text.append(heading.text.strip())
        for paragraph in paragraphs:
            extracted_text.append(paragraph.text.strip())

        readable_text = "\n\n".join(extracted_text)

        return readable_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during scraping or parsing: {e}")
        return None

if __name__ == "__main__":
    target_url = input("Enter the URL you want to scrape: ")
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    parsed_data = scrape_and_parse_text(target_url)

    if parsed_data:
        print("\n--- Scraped and Parsed Text ---")
        print(parsed_data)
    else:
        print("Failed to scrape and parse text from the URL.")
