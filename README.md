# Chanda Identifier

This project is a Chanda (meter) identifier for Sanskrit verses. It uses various libraries to process and identify the meter of given Sanskrit text.

## Requirements

To install the required dependencies, run:

```sh
pip install -r requirements.txt
```
## Usage
### Initialization
To initialize the Chanda engine, specify the path to the data directory:

```py
from chanda import Chanda

chanda_engine = Chanda(data_path="data")
```

### Identify Chanda
To identify the Chanda of a given Sanskrit verse:

```py
sloka = "तपःस्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।\nनारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम् ॥"
result = chanda_engine.identify_from_text(sloka, verse=True, fuzzy=False)
```

### Extract Results
To extract and display the results:

```py
import json

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

        line_info = {
            "text": line_text,
            "laghu_guru": display_lg,
            "gana": display_gana
        }
        verse_info["lines"].append(line_info)

    verse_chanda_info.append(verse_info)

print(json.dumps(verse_chanda_info, ensure_ascii=False, indent=2))
```

## Data Files
The data directory should contain the following CSV files:

- `chanda_jaati.csv`
- `chanda_sama.csv`
- `chanda_ardhasama.csv`
- `chanda_vishama.csv`
