import json
from chanda import Chanda
from tqdm import tqdm

def identify_chanda_for_slokas(json_path, output_path, data_path="data", verse=True, fuzzy=False):
    # Load sloka JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        sloka_data = json.load(f)

    chanda_engine = Chanda(data_path=data_path)

    for sloka_obj in tqdm(sloka_data, desc="Processing Slokas", unit="sloka"):
        padas = sloka_obj.get("padas", [])
        if len(padas) < 2:
            sloka_obj["chanda"] = None
            sloka_obj["guru_laghu"] = []
            sloka_obj["gana"] = []
            continue

        # Join all words in all padas
        lines = []
        for pada in padas:
            line = " ".join(word_obj["word"].strip() for word_obj in pada)
            lines.append(line.strip())

        full_sloka = "\n".join(lines)

        try:
            result = chanda_engine.identify_from_text(full_sloka, verse=verse, fuzzy=fuzzy)
            verse_results = result["result"]["verse"]
            line_results = result["result"]["line"]

            # Chanda label
            if verse_results and verse_results[0]["chanda"]:
                sloka_obj["chanda"] = " / ".join(verse_results[0]["chanda"][0])
            else:
                sloka_obj["chanda"] = "Unknown"

            # Guru-Laghu and Gana
            guru_laghu = []
            gana_list = []
            for line_id in verse_results[0]["lines"]:
                line = line_results[line_id]["result"]
                lg_seq = ''.join(line["display_lg"])
                gana = line["display_gana"]
                guru_laghu.append(lg_seq)
                gana_list.append(gana)

            sloka_obj["guru_laghu"] = guru_laghu
            sloka_obj["gana"] = gana_list

        except Exception as e:
            sloka_obj["chanda"] = f"Error: {str(e)}"
            sloka_obj["guru_laghu"] = []
            sloka_obj["gana"] = []

    # Save updated JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sloka_data, f, ensure_ascii=False, indent=2)

# Example usage
identify_chanda_for_slokas("slokas.json", "slokas_with_chanda.json")
