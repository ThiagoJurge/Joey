import json 
import re 


arq = open('grupos.json', 'r')
data = json.load(arq)
pattern = re.compile(r"\b\d{7,8}\b")

# Iterando sobre a lista de dicionários para encontrar correspondências
matches = []
for entry in data:
    found = pattern.findall(entry['group_name'])
    if found:
        matches.append({'group_id': entry['group_id'], 'matches': found})

# Exibindo as correspondências
for match in matches:
    print(f"Group ID: {match['group_id']}, Grupo ID: {', '.join(match['matches'])}")