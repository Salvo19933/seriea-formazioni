import requests
from bs4 import BeautifulSoup
import os

TEAMS = ["Juventus","Inter","Milan","Napoli","Roma","Lazio","Atalanta","Fiorentina","Bologna","Torino","Verona","Monza","Udinese","Empoli","Salernitana","Lecce","Sassuolo","Genoa","Spezia","Frosinone"]

DATA = []

for team in TEAMS:
    url = f"https://www.fantacalcio.it/giocatori/probabili-formazioni/serie-a/{team.lower()}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    mod = soup.select_one(".formazioneHeader .modulo").text.strip()
    players = [p.text.strip() for p in soup.select(".formazione__lista li.titolare")]
    DATA.append({"team": team, "modulo": mod, "players": players})

html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Formazioni Serie A</title><style>body{font-family:sans-serif;} .team{margin-bottom:20px;} img{vertical-align:middle;width:40px;} h2{display:inline-block;margin-left:10px;}</style></head><body>'
for d in DATA:
    logo_path = f"logos/{d['team'].lower()}.png"
    html += f'<div class="team"><img src="{logo_path}" alt="{d["team"]} logo"><h2>{d["team"]} — {d["modulo"]}</h2><ul>'
    for p in d["players"]:
        html += "<li>" + p + "</li>"
    html += "</ul></div>"
html += "</body></html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
