import requests
from bs4 import BeautifulSoup
import subprocess as sp

cache_path = "/home/s1/chanwoopark/dataset_scripts/kowikitext/cache/done.txt"


def main():
    with open(cache_path) as f:
        done = f.read().split("\n")
    done = set([x.strip() for x in done])
    url = "https://dumps.wikimedia.org/kowiki/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    selector = "body > pre > a"
    tags = soup.select(selector)

    for tag in tags:
        content = tag.get_text()
        if content.startswith("latest"):
            continue
        if ".." in content:
            continue
        content = content.replace("/", "")
        if content in done:
            continue
        print(f"Downloading {content}")
        wsp = "/home/s1/chanwoopark/dataset_scripts/kowikitext/scripts"
        cmd = f"cd {wsp} && bash pipeline.sh {content}"
        sp.run(cmd, shell=True)
        with open(cache_path, "a") as f:
            f.write(f"{content}\n")


if __name__ == "__main__":
    main()
