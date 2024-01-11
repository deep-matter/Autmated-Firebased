import json
import os

def parse(file_path):
    current_config = {}
    current_index = 1
    output_folder = "apps"  # Folder name where JSON configurations will be saved

    os.makedirs(output_folder, exist_ok=True)

    with open(file_path, 'r') as file:
        for line in file:
            # Check if the line contains ':'
            if ':' in line:
                key, value = map(str.strip, line.split(':', 1))

                value = value.split('"')[1]

                if value.endswith('.'):
                    value = value[:-1].strip()

                current_config[key] = value
            elif line.strip().lower() == "next":
                if current_config:
                    json_config = json.dumps(current_config, indent=2, ensure_ascii=False)
                    output_file_path = os.path.join(output_folder, f"app_{current_index}.json")
                    with open(output_file_path, 'w') as json_file:
                        json_file.write(json_config)
                    print(f"JSON configuration for app_{current_index} saved to {output_file_path}")

                    current_config = {}
                    current_index += 1

    if current_config:
        json_config = json.dumps(current_config, indent=2, ensure_ascii=False)
        output_file_path = os.path.join(output_folder, f"app_{current_index}.json")
        with open(output_file_path, 'w') as json_file:
            json_file.write(json_config)
        print(f"JSON configuration for app_{current_index} saved to {output_file_path}")

parse("configs.txt")
