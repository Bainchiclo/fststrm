import requests

def create_m3u_from_url(input_url, output_file):
    response = requests.get(input_url, timeout=15)
    response.raise_for_status()  # stop if download fails

    lines = response.text.splitlines()

    with open(output_file, "w", encoding="utf-8") as outfile:
        # M3U header
        outfile.write("#EXTM3U\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            try:
                name, url = line.split(",", 1)
                outfile.write(f"#EXTINF:-1,{name}\n")
                outfile.write(f"{url}\n")
            except ValueError:
                print(f"Skipping invalid line: {line}")


if __name__ == "__main__":
    INPUT_URL = "https://raw.githubusercontent.com/yuanwangokk-1/TV-BOX/refs/heads/main/Jsm/json/%E2%9C%A8live%E2%9C%A8.txt"  # <-- your text file URL
    OUTPUT_FILE = "textm3u.m3u8"

    create_m3u_from_url(INPUT_URL, OUTPUT_FILE)
    print("M3U playlist created:", OUTPUT_FILE)
