import requests

def fetch_lines(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text.splitlines()


def create_m3u_from_sources(sources, output_file):
    """
    sources = [
        ("Source I", "https://raw.githubusercontent.com/yuanwangokk-1/TV-BOX/refs/heads/main/Jsm/json/%E2%9C%A8live%E2%9C%A8.txt"),
        ("Source 2", "https://raw.githubusercontent.com/ffmking/tv1/c0a72145a8afed0f879b98d44ae29dc7e18467e6/1816.txt"),
        ("Source 3", "https://raw.githubusercontent.com/hang888888/hang88/27856b64a8007d9e6cd977c1301b662b0a4f3f59/eztv.txt")
    ]
    """

    seen_urls = set()

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("#EXTM3U\n")

        for group_name, url in sources:
            print(f"Fetching {group_name}: {url}")

            try:
                lines = fetch_lines(url)
            except requests.RequestException as e:
                print(f"Failed to fetch {url}: {e}")
                continue

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                try:
                    name, stream_url = line.split(",", 1)

                    # Skip duplicate streams
                    if stream_url in seen_urls:
                        continue

                    seen_urls.add(stream_url)

                    outfile.write(
                        f'#EXTINF:-1 group-title="{group_name}",{name}\n'
                    )
                    outfile.write(f"{stream_url}\n")

                except ValueError:
                    print(f"Skipping invalid line: {line}")


if __name__ == "__main__":
    SOURCES = [
        (
            "Source 1",
            "https://raw.githubusercontent.com/yuanwangokk-1/TV-BOX/refs/heads/main/Jsm/json/%E2%9C%A8live%E2%9C%A8.txt"
        ),
        (
            "Source 2",
            "https://raw.githubusercontent.com/ffmking/tv1/c0a72145a8afed0f879b98d44ae29dc7e18467e6/1816.txt"
        ),
         (
            "Source 3",
            "https://raw.githubusercontent.com/hang888888/hang88/27856b64a8007d9e6cd977c1301b662b0a4f3f59/eztv.txt"
        )
    ]

    OUTPUT_FILE = "textm3u.m3u8"

    create_m3u_from_sources(SOURCES, OUTPUT_FILE)
    print("M3U playlist created:", OUTPUT_FILE)
