import json
from chanda import Chanda

# Load tarkasangraha.json
with open("tarkasangraha.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Define your existing chanda identification function
def identify_chanda(sloka, data_path="data", verse=True, fuzzy=False):
    chanda_engine = Chanda(data_path=data_path)
    result = chanda_engine.identify_from_text(sloka, verse=verse, fuzzy=fuzzy)

    verse_results = result["result"]["verse"]
    line_results = result["result"]["line"]

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
            verse_info["lines"].append({
                "text": line_text,
                "laghu_guru": display_lg,
                "gana": display_gana
            })
        verse_chanda_info.append(verse_info)

    return verse_chanda_info

# Helper: Combine all words in a sloka into a full string
def get_combined_sloka_text(sloka_obj):
    lines = []
    for pada in sloka_obj.get("padas", []):
        words = [w["word"].strip() for w in pada.get("words", [])]
        lines.append(" ".join(words))
    return " ".join(lines).replace(" ।", "।").replace(" ॥", "॥").strip()

# Add chandas info to each sloka
for sloka_obj in data:
    sloka_text = get_combined_sloka_text(sloka_obj)
    try:
        chandas_info = identify_chanda(sloka_text)
        sloka_obj["chandas"] = chandas_info  # Add new field
    except Exception as e:
        sloka_obj["chandas"] = {"error": str(e)}

# Save updated file
with open("tarkasangraha_chandas.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
