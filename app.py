from flask import Flask, render_template, jsonify
import re

app = Flask(__name__)

# Load the synergies data from the file
def load_synergies(synergies_file):
    synergies_dict = {}
    with open(synergies_file, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r"^(.*): Jokers: (.*)$", line)
            if match:
                joker_name = match.group(1).strip()
                synergies = match.group(2).split(', ')
                synergies_dict[joker_name] = synergies
    return synergies_dict

synergies_file = "corrected_joker_synergies.txt"  # The file with your joker synergies
synergies_data = load_synergies(synergies_file)  # Load the data

# Flask route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Serve the index.html template

# Flask route to fetch synergies for a specific joker
@app.route('/synergies/<joker_name>')
def get_synergies(joker_name):
    joker_name = joker_name.strip()
    if joker_name == "all":
        return jsonify(synergies_data)
    elif joker_name in synergies_data:
        return jsonify({joker_name: synergies_data[joker_name]})
    else:
        return jsonify({'error': 'Joker not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
