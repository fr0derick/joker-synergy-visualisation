import re

# Define the jokers that should not be part of each other's synergies
related_jokers = {'Crafty Joker', 'Clever Joker', 'Sly Joker', 'Wily Joker', 'Devious Joker'}

# Function to remove related jokers from specific joker synergy lists but keep the original joker
def clean_jokers_line(joker_name, joker_synergies):
    # Remove other related jokers from the synergies, but keep the original joker
    cleaned_synergies = [j for j in joker_synergies if j not in related_jokers or j == joker_name]
    return cleaned_synergies

# Load the compiled synergy file
synergies_file = "final_complete_joker_synergies_fixed.txt"
output_file = "corrected_joker_synergies.txt"

with open(synergies_file, 'r', encoding='utf-8') as file:
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for line in file:
            # Match lines that contain jokers and their synergies
            match = re.match(r"^(.*): Jokers: (.*)$", line)
            if match:
                joker_name = match.group(1).strip()  # Extract the joker name
                synergies = match.group(2).split(', ')  # Split the synergies into a list
                
                # Clean the synergies if the joker is in the related_jokers set
                cleaned_synergies = clean_jokers_line(joker_name, synergies)
                
                # Write the cleaned line back to the file
                if cleaned_synergies:
                    out_file.write(f"{joker_name}: Jokers: {', '.join(cleaned_synergies)}\n")
                else:
                    out_file.write(f"{joker_name}: Jokers: No synergies\n")
            else:
                # If the line doesn't match the expected format, write it as is
                out_file.write(line)

print("Corrections applied and saved to corrected_joker_synergies.txt")
