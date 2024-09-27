import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time

# Step 1: Fetch the central joker list from the category page
category_url = "https://balatrogame.fandom.com/wiki/Category:Jokers"
response = requests.get(category_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all joker links that match the URL pattern ending with _(Joker)
joker_links = soup.find_all('a', href=True)
joker_urls = []

# Filter links to only those that end with _(Joker)
for link in joker_links:
    if link['href'].endswith("_(Joker)"):
        joker_url = "https://balatrogame.fandom.com" + link['href']
        joker_urls.append(joker_url)

# Remove duplicates by converting the list to a set and back to a list
joker_urls = list(set(joker_urls))  # This removes duplicate URLs

print(f"Found {len(joker_urls)} unique jokers.")

# Function to fetch Wikitext for each joker URL
def get_wikitext_for_joker(url):
    edit_url = url + "?action=edit"
    response = requests.get(edit_url)
    if "wpTextbox1" in response.text:
        soup = BeautifulSoup(response.text, 'html.parser')
        wikitext_area = soup.find('textarea', {'id': 'wpTextbox1'})
        if wikitext_area:
            return url, wikitext_area.text
    return url, None

# Function to extract synergy and anti-synergy text from Wikitext
def extract_synergy_text(wikitext):
    synergy_section = ""
    anti_synergy_section = ""

    lines = wikitext.split('\n')
    in_synergy = False
    in_anti_synergy = False

    for line in lines:
        if "===[[Jokers]]===" in line:
            in_synergy = True
            in_anti_synergy = False
            continue
        
        if "anti-synergy" in line.lower():
            in_anti_synergy = True
            in_synergy = False
            continue

        if in_synergy and line.startswith("*"):
            synergy_section += line + "\n"

        if in_anti_synergy and line.startswith("*"):
            anti_synergy_section += line + "\n"
    
    return synergy_section.strip(), anti_synergy_section.strip()

# Step 4: Use concurrent futures to fetch multiple joker pages at the same time
with open('joker_synergies.txt', 'w', encoding='utf-8') as file:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the fetching tasks
        future_to_url = {executor.submit(get_wikitext_for_joker, url): url for url in joker_urls}

        # As the results come in, process them
        for future in concurrent.futures.as_completed(future_to_url):
            url, wikitext = future.result()
            joker_name = url.split('/')[-1].replace('_', ' ').replace('(Joker)', '').strip()

            if wikitext:
                synergy_text, anti_synergy_text = extract_synergy_text(wikitext)
                file.write(f"Joker: {joker_name}\n")
                file.write("Synergies:\n")
                file.write(synergy_text + "\n\n")
                file.write("Anti-synergies:\n")
                file.write(anti_synergy_text + "\n\n")
                print(f"Scraped synergies for {joker_name}.")
