import json
from collections import defaultdict
from tqdm import tqdm

def restructure_json(data):
    grouped_by_sarga = defaultdict(list)

    # Step 1: Group by (kanda, sarga)
    for entry in tqdm(data, desc="Grouping slokas by sarga"):
        key = (entry["kanda"], entry["sarga"])
        grouped_by_sarga[key].append(entry)

    final_output = []

    # Step 2: Process each Sarga
    for (kanda, sarga), slokas in tqdm(grouped_by_sarga.items(), desc="Processing each sarga"):
        new_slokas = []
        i = 0
        sloka_counter = 1

        while i < len(slokas):
            current = slokas[i]

            if len(current["padas"]) == 1 and (i + 1 < len(slokas)):
                next_sloka = slokas[i + 1]

                # Merge current pada(s) as prefix to next sloka's padas
                merged_padas = current["padas"] + next_sloka["padas"]

                # Assign sloka number and update all words
                for pada_idx, pada in enumerate(merged_padas):
                    for word in pada:
                        word["sloka"] = sloka_counter
                        word["pada"] = pada_idx

                new_slokas.append({
                    "kanda": kanda,
                    "sarga": sarga,
                    "padas": merged_padas,
                    "sloka": sloka_counter,
                    "chanda": next_sloka.get("chanda"),
                    "guru_laghu": next_sloka.get("guru_laghu", []),
                    "gana": next_sloka.get("gana", [])
                })

                sloka_counter += 1
                i += 2  # skip next since it's already merged

            else:
                # Keep current sloka as is, just update sloka number and padas
                for pada_idx, pada in enumerate(current["padas"]):
                    for word in pada:
                        word["sloka"] = sloka_counter
                        word["pada"] = pada_idx

                current["sloka"] = sloka_counter
                new_slokas.append(current)
                sloka_counter += 1
                i += 1

        final_output.extend(new_slokas)

    return final_output


# Example usage
if __name__ == "__main__":
    with open("slokas_with_chanda.json", "r", encoding="utf-8") as f:
        input_data = json.load(f)

    output_data = restructure_json(input_data)

    with open("slokas_with_chanda_formatted.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
