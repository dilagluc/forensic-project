import re

def extract_lines_with_keywords(text):
    # Définition du pattern regex
    #pattern = re.compile(r".*/Windows/System32/config.*\b(?:SAM(?:\.LOG\d*)?|SECURITY(?:\.LOG\d*)?)|SOFTWARE(?:\.LOG\d*)?)|SYSTEM)(?:\.LOG\d*)?)\b", re.MULTILINE | re.IGNORECASE)
    pattern = re.compile(r".*/Windows/System32/config.*\b(?:SAM|SECURITY|SOFTWARE|SYSTEM)", re.IGNORECASE)
    # Recherche de toutes les correspondances
    matches = pattern.findall(text)
    
    return matches

# Exemple d'utilisation
texte = """
Ceci est une ligne contenant Windows SAM
Une autre ligne contenant SYSTEM et Windows
Ligne avec SOFTWARE à la fin mais pas de Windows
Ceci est une ligne avec SECURITY Windows
Windows/iuser/SECURITY
/Windows/System32/config/SAM
/Windows/System32/config/SECURITY
/Windows/System32/config/SOFTWARE
/Windows/System32/config/SYSTEM
aaaaaaaaa/Windows/System32/config/SYSTEM.LOG jrfhtfjh
/Windows/System32/config/SYSTEM fgdfyegiyfey
/Windows/System32/config/drydtfru
"""

lignes_correspondantes = extract_lines_with_keywords(texte)
print("Lignes contenant 'Windows' et se terminant par 'SAM', 'SECURITY', 'SOFTWARE' ou 'SYSTEM':")
for ligne in lignes_correspondantes:
    print(ligne)




'''import yaml

yaml_data = """
- name: SYSTEM_FILE
  path: null
  out: |
    - regb: "/Windows/System32/config/RegBack/SAM"
      dest_dir: "/Registry/RegBack/"
      isRecursive: false
      stringToMatch: "UsrClass"
"""

parsed_data = yaml.safe_load(yaml_data)

for entry in parsed_data:
    if entry['name'] == 'SYSTEM_FILE':
        print("Name:", entry['name'])
        print("Path:", entry['path'])
        print("Out:")
        items = yaml.safe_load(entry['out'])
        for item in items:
            print(item)
            for key, value in item.items():
                print("  {}: {}".format(key, value))'''
