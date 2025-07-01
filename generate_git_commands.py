#!/usr/bin/env python3
"""
Script som genererar git-kommandon baserat på SFS JSON-filer.
Loopar igenom alla JSON-filer i mappen "sfs" och skapar markdown-filer
från författningstexten samt git commit-kommandon med utfärdandedatum som author date.
"""

import json
import glob
import os
from datetime import datetime

def clean_text(text):
    """Rengör texten genom att ersätta \\r\\n med vanliga radbrytningar."""
    if text:
        return text.replace("\\r\\n", "\n").replace("\r\n", "\n")
    return text

def create_markdown_file(data, json_filename):
    """Skapar en markdown-fil från JSON-data."""
    # Skapa markdown-filnamn baserat på JSON-filnamn
    base_name = os.path.splitext(os.path.basename(json_filename))[0]
    markdown_filename = f"markdown/{base_name}.md"

    # Skapa markdown-mappen om den inte finns
    os.makedirs("markdown", exist_ok=True)

    # Hämta data för markdown-filen
    beteckning = data.get("beteckning", "Okänd beteckning")
    rubrik = data.get("rubrik", "Ingen rubrik")
    forfattningstext = ""

    if "fulltext" in data and "forfattningstext" in data["fulltext"]:
        forfattningstext = clean_text(data["fulltext"]["forfattningstext"])

    # Skapa markdown-innehåll
    markdown_content = f"# {beteckning}\n\n"
    markdown_content += f"## {rubrik}\n\n"

    if forfattningstext:
        markdown_content += forfattningstext
    else:
        markdown_content += "*Ingen författningstext tillgänglig*"

    # Skriv markdown-filen
    with open(markdown_filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    return markdown_filename

def generate_git_commands():
    """Genererar git-kommandon för alla SFS JSON-filer."""

    # Hitta alla JSON-filer i sfs mappen
    json_files = glob.glob("sfs/*.json")

    if not json_files:
        print("Inga JSON-filer hittades i mappen sfs/")
        return

    # Sortera filerna för konsistent ordning
    json_files.sort()

    # Öppna output-filen för att skriva git-kommandon
    with open("git_commands.sh", "w", encoding="utf-8") as output_file:
        output_file.write("#!/bin/bash\n")
        output_file.write("# Genererade git-kommandon för SFS-filer\n")
        output_file.write("# Genererat: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        processed_count = 0
        skipped_count = 0

        for json_file in json_files:
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Hämta utfärdandedatum från fulltext.utfardadDateTime
                if "fulltext" in data and "utfardadDateTime" in data["fulltext"]:
                    utfardad_datetime = data["fulltext"]["utfardadDateTime"]
                    
                    if utfardad_datetime:
                        # Skapa markdown-fil från författningstexten
                        markdown_file = create_markdown_file(data, json_file)

                        # Konvertera ISO datetime till git-format
                        dt = datetime.fromisoformat(utfardad_datetime.replace("Z", "+00:00"))
                        git_date = dt.strftime("%Y-%m-%d %H:%M:%S %z")
                        
                        # Hämta beteckning och rubrik för commit-meddelandet
                        beteckning = data.get("beteckning", "Okänd beteckning")
                        rubrik = data.get("rubrik", "Ingen rubrik")
                        
                        # Skapa commit-meddelande
                        commit_message = f"Add {beteckning}: {rubrik}"
                        
                        # Skapa git commit-kommando som bara lägger till markdown-filen
                        git_command = f'git add "{markdown_file}" && git commit --author-date="{git_date}" -m "{commit_message}"\n'
                        
                        output_file.write(git_command)
                        processed_count += 1
                        
                        print(f"Processerad: {json_file} -> {markdown_file} - {beteckning}")
                    else:
                        print(f"Ingen utfärdandedatum i: {json_file}")
                        skipped_count += 1
                else:
                    print(f"Ingen fulltext.utfardadDateTime i: {json_file}")
                    skipped_count += 1
                    
            except json.JSONDecodeError as e:
                print(f"Fel vid läsning av JSON i {json_file}: {e}")
                skipped_count += 1
            except (KeyError, ValueError, TypeError) as e:
                print(f"Oväntat fel vid bearbetning av {json_file}: {e}")
                skipped_count += 1
        
        print("\nSammanfattning:")
        print(f"Processerade filer: {processed_count}")
        print(f"Överhoppade filer: {skipped_count}")
        print(f"Totalt antal filer: {len(json_files)}")
        print("Git-kommandon sparade i: git_commands.sh")

if __name__ == "__main__":
    generate_git_commands()
