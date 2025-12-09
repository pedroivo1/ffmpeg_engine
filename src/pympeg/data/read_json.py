from pathlib import Path
import json

BASE_DIR = Path(__file__).parent

JSON_PATH = BASE_DIR / "flags.json"


def carregar_flags():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    all_flags = carregar_flags()
    # pprint(all_flags['global_options'])
    # pprint(all_flags['input_options'])
    # pprint(all_flags['output_options'])

    if all_flags:
        flags_globais = [item["flag"] for item in all_flags["global_options"]]
        flags_entrada = [item["flag"] for item in all_flags["input_options"]]
        flags_saida = []

        for sub_lista_opcoes in all_flags["output_options"].values():
            flags_saida.extend([item["flag"] for item in sub_lista_opcoes])

        print("--- Global Options ---")
        print(flags_globais)

        print("\n--- Input Options ---")
        print(flags_entrada)

        print("\n--- Output Options ---")
        print(flags_saida)

global_options = ["-y", "-n", "-hide_banner", "-loglevel", "-stats", "-version"]
input_options = ["-i", "-f", "-ss", "-t", "-stream_loop", "-re"]
output_options = [
    "-c:v",
    "-b:v",
    "-crf",
    "-vf",
    "-r",
    "-vn",
    "-aspect",
    "-preset",
    "-c:a",
    "-b:a",
    "-an",
    "-ar",
    "-ac",
    "-af",
    "-f",
    "-t",
    "-fs",
    "-map",
    "-shortest",
    "-movflags",
]
