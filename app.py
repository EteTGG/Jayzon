from flask import Flask, render_template, url_for
import json
import os

app = Flask(__name__)

# Load JSON data for characters
def load_characters():
    try:
        with open("characters.json", "r") as f:
            return json.load(f).get("characters", [])
    except FileNotFoundError:
        print("Error: characters.json not found")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode characters.json")
        return []

characters = load_characters()

# Load universe data from universes.json
def load_universe_data():
    try:
        with open('universes.json', 'r') as file:
            data = json.load(file)
            universes = data.get('universes', [])
            if not universes:
                print("Warning: No universes loaded!")
            return universes
    except FileNotFoundError:
        print("Error: universes.json not found")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode universes.json")
        return []



@app.route("/multiverse")
def multiverse():
    """Multiverse overview page."""
    universes = load_universe_data()  # Load universe data from universes.json
    return render_template("multiverse.html", multiverse=universes)

@app.route("/")
def index():
    """Homepage with a list of all characters."""
    return render_template("index.html", characters=characters)


@app.route("/character/<name>")
def character(name):
    """Detail page for a specific character."""
    character_data = next((c for c in characters if c["name"] == name), None)
    if character_data:
        # Find the universe associated with this character
        universe_data = None
        if 'universe_number' in character_data:
            universe_data = next(
                (u for u in load_universe_data() if u['designation_number'] == character_data.get('universe_number')), 
                None
            )
        
        return render_template("character.html", character=character_data, universe=universe_data)
    else:
        return "Character not found", 404



@app.route('/universe/<int:universe_number>')
def universe_details(universe_number):
    """Detail page for a specific universe."""
    try:
        universes = load_universe_data()
        universe = next(
            (u for u in universes if u['designation_number'] == universe_number),
            None
        )
        
        if universe:
            # Verify image exists
            image_path = os.path.join(
                app.static_folder, 'images', universe.get('images', '')
            )
            universe['image_exists'] = os.path.exists(image_path)
            
            # Render universe details template
            return render_template('universe_details.html', universe=universe)
        else:
            return "Universe not found", 404
    except Exception as e:
        print(f"Error loading universe {universe_number}: {str(e)}")
        return "Error loading universe details", 500

if __name__ == "__main__":
    app.run(debug=True)
