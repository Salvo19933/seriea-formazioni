import requests
from bs4 import BeautifulSoup
import os

TEAMS = ["Juventus", "Inter", "Milan", "Napoli", "Roma", "Lazio", "Atalanta", "Fiorentina", "Bologna", "Torino", "Verona", "Monza", "Udinese", "Empoli", "Salernitana", "Lecce", "Sassuolo", "Genoa", "Spezia", "Frosinone"]

DATA = []

# Loop through each team to scrape data
for team in TEAMS:
    try:
        # Construct the URL for the team's probable formation page
        url = f"https://www.fantacalcio.it/giocatori/probabili-formazioni/serie-a/{team.lower().replace(' ', '-')}" # Handle spaces in team names for URL
        r = requests.get(url)
        r.raise_for_status() # Raise an exception for HTTP errors
        soup = BeautifulSoup(r.text, "html.parser")

        # Extract the formation module (e.g., 4-3-3)
        # Check if the element exists before accessing .text
        mod_element = soup.select_one(".formazioneHeader .modulo")
        mod = mod_element.text.strip() if mod_element else "N/D"

        # Extract the starting players
        # Check if the elements exist
        players_elements = soup.select(".formazione__lista li.titolare")
        players = [p.text.strip() for p in players_elements]
        
        DATA.append({"team": team, "modulo": mod, "players": players})
    except requests.exceptions.RequestException as e:
        print(f"Errore durante lo scraping per {team}: {e}")
        DATA.append({"team": team, "modulo": "Errore", "players": ["Dati non disponibili"]})
    except Exception as e:
        print(f"Si è verificato un errore inatteso per {team}: {e}")
        DATA.append({"team": team, "modulo": "Errore", "players": ["Dati non disponibili"]})

# Start HTML content with Tailwind CSS and Inter font
html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formazioni Serie A</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f0f2f5; /* Light gray background */
        }}
    </style>
</head>
<body class="p-4 bg-gray-100 flex flex-col items-center min-h-screen">
    <div class="container mx-auto max-w-4xl">
        <h1 class="text-4xl font-bold text-center text-gray-800 mb-8 rounded-lg p-4 bg-white shadow-md">
            Probabili Formazioni Serie A
        </h1>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
"""

# Iterate through the scraped data to generate HTML for each team
for d in DATA:
    # Use a placeholder image for logos. Replace with your actual logo paths in 'logos/' directory
    # Example for a real logo: logo_path = f"logos/{d['team'].lower().replace(' ', '-')}.png"
    # Placeholder: https://placehold.co/{width}x{height}/{background color in hex}/{text color in hex}?text={text}
    logo_path = f"https://placehold.co/40x40/cbd5e1/4b5563?text={d['team'][0].upper()}" # Placeholder with first letter of team

    # Create a card for each team
    html += f"""
            <div class="team bg-white shadow-lg rounded-lg p-6 mb-4 transform transition-transform duration-300 hover:scale-105 hover:shadow-xl">
                <div class="flex items-center mb-4">
                    <img src="{logo_path}" alt="{d['team']} logo" class="w-10 h-10 rounded-full mr-4 border-2 border-gray-200 object-contain">
                    <h2 class="text-2xl font-semibold text-gray-700">{d['team']} — {d['modulo']}</h2>
                </div>
                <ul class="list-disc list-inside text-gray-600 space-y-2">
    """
    # Add players to the list
    for p in d["players"]:
        html += f"""
                    <li class="flex items-center">
                        <svg class="w-4 h-4 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                        </svg>
                        {p}
                    </li>
        """
    html += """
                </ul>
            </div>
    """

html += """
        </div>
    </div>
    <footer class="mt-8 text-center text-gray-500 text-sm">
        Dati forniti da Fantacalcio.it
    </footer>
</body>
</html>
"""

# Write the generated HTML to index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
