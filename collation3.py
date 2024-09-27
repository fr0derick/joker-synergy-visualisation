import re
from collections import defaultdict
import urllib.parse

# Function to extract jokers mentioned using the {{J|Joker_Name}} or {{j|Joker_Name}} format
def extract_synergized_jokers(synergy_text):
    # Capture both uppercase and lowercase 'J' or 'j' for jokers
    jokers_found = re.findall(r"\{\{[Jj]\|([^\}]+)\}\}", synergy_text)
    # Decode URL-encoded characters (e.g., S%C3%A9ance -> Séance)
    decoded_jokers = [urllib.parse.unquote(joker_name) for joker_name in jokers_found]
    return decoded_jokers

# Function to extract tarot cards mentioned using the {{hl|purple|...}} format
def extract_tarot_cards(synergy_text):
    # Capture tarot cards in the {{hl|purple|Tarot_Card}} format
    tarot_found = re.findall(r"\{\{hl\|purple\|([^\}]+)\}\}", synergy_text)
    return tarot_found

# Load the scraped synergy text file
synergies_file = "joker_synergies.txt"  # Replace with your actual file
synergies_dict = defaultdict(set)  # Store synergies as a dictionary of sets for no duplicates
tarot_dict = defaultdict(set)  # Store tarot cards separately

with open(synergies_file, 'r', encoding='utf-8') as file:
    current_joker = None  # The joker whose synergies we are reading
    
    for line in file:
        # Identify the joker name from lines starting with "Joker: "
        if line.startswith("Joker: "):
            current_joker = line.split(": ")[1].strip()
        
        # If we're reading a synergies section, extract jokers and tarot cards mentioned
        elif current_joker and "Synergies:" in line:
            # Read subsequent lines for synergies until the next joker section or end
            synergy_text = ""
            for next_line in file:
                if next_line.startswith("Joker: ") or "Anti-synergies:" in next_line:
                    break  # Stop reading synergies when we encounter a new joker or anti-synergy section
                synergy_text += next_line
            
            # Extract all joker names from the synergy section
            synergized_jokers = extract_synergized_jokers(synergy_text)
            synergies_dict[current_joker].update(synergized_jokers)  # Add found synergies to current joker

            # Extract all tarot cards from the synergy section
            tarot_cards = extract_tarot_cards(synergy_text)
            tarot_dict[current_joker].update(tarot_cards)  # Add found tarot cards to current joker

# Step 2: Ensure reverse (bi-directional) synergies for jokers, but not tarot cards
for joker, joker_synergies in synergies_dict.items():
    for synergized_joker in joker_synergies:
        if synergized_joker in synergies_dict:  # Ensure synergized joker is in the dictionary
            synergies_dict[synergized_joker].add(joker)  # Add the reverse synergy

# Step 3: Write the complete synergy list (with separate tarot cards) to a text file
with open('final_complete_joker_synergies_fixed.txt', 'w', encoding='utf-8') as out_file:
    for joker, joker_synergies in synergies_dict.items():
        synergy_list = ', '.join(sorted(joker_synergies)) if joker_synergies else "No synergies"
        tarot_list = ', '.join(sorted(tarot_dict[joker])) if tarot_dict[joker] else None
        
        # Write the joker synergies and tarot cards separately, omit tarot cards if none exist
        if tarot_list:
            out_file.write(f"{joker}: Jokers: {synergy_list} | Tarot Cards: {tarot_list}\n")
        else:
            out_file.write(f"{joker}: Jokers: {synergy_list}\n")

print("Final complete synergy list with tarot cards saved to final_complete_joker_synergies_fixed.txt")
