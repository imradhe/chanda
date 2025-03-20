import json
from chanda import Chanda

def identify_chanda(sloka, data_path="data", verse=True, fuzzy=False):
    # Initialize Chanda Engine
    chanda_engine = Chanda(data_path=data_path)

    # Identify Chanda
    result = chanda_engine.identify_from_text(sloka, verse=verse, fuzzy=fuzzy)

    # Extract results
    verse_results = result["result"]["verse"]
    line_results = result["result"]["line"]

    # Build JSON
    verse_chanda_info = []

    for verse_idx, verse in enumerate(verse_results):
        verse_info = {
            "verse_number": verse_idx + 1,
            "chanda": " / ".join(verse["chanda"][0]) if verse["chanda"] else "Unknown",
            "lines": []
        }

        for line_id in verse["lines"]:
            line = line_results[line_id]
            line_text = line["line"].strip()
            display_lg = ''.join(line["result"]["display_lg"])
            display_gana = line["result"]["display_gana"]

            line_info = {
                "text": line_text,
                "laghu_guru": display_lg,
                "gana": display_gana
            }
            verse_info["lines"].append(line_info)

        verse_chanda_info.append(verse_info)

    return json.dumps(verse_chanda_info, ensure_ascii=False, indent=2)

# Example usage
sloka = "तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।\nनारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"
print(identify_chanda(sloka))

