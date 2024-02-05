import os
import re
import xmltodict
import wikitextparser as wtp
from tqdm import tqdm
from argparse import ArgumentParser
import multiprocessing as mp
import json

from normalizer import text_preprocess, text_postprocess, title_preprocess


BANNED_START = ["모듈:", "위키백과:", "틀:", "분류:", "파일:", "미디어위키:"]


def transform_page_to_wikitext(page):
    title = page["title"]
    entry = {}
    entry["title"] = title

    for banned in BANNED_START:
        if title.startswith(banned):
            return None

    try:
        sections = wtp.parse(page["revision"]["text"]["#text"]).sections
        wikitext = []

        first_section_text = sections[0].plain_text()
        if first_section_text and first_section_text[0] != "=":
            lines = first_section_text.split("\n")
            lines = [text_preprocess(line) for line in lines]
            first_section_text = text_postprocess("\n".join(lines))
            wikitext.append(f"{first_section_text}\n")

        for section in sections[1:]:
            section_title = section.title.strip()
            if section_title is not None:
                section_title = section_title.strip()
            if (
                (section_title is None)
                or (section_title in ["같이 보기", "각주", "참고 문헌", "외부 링크"])
                or (not section_title)
            ):
                continue
            plain_text = section.plain_text()
            lines = plain_text.split("\n")
            level = 0
            if lines:
                level = lines[0].split()[0].count("=")
            if level == 0 or level >= 3:
                continue
            lines = [text_preprocess(line) for line in lines]
            text = text_postprocess("\n".join(lines)).strip()
            if not text:
                continue
            wikitext.append(f"\n\n{text}\n\n")
        wikitext = "".join(wikitext)
        wikitext = re.sub("\n{3,}", "\n\n", wikitext).strip()
        if not wikitext:
            return None
        if wikitext.count("\n") <= 4 and (
            ("#REDIRECT" in wikitext)
            or ("#넘겨주기" in wikitext)
            or ("#redirect" in wikitext)
        ):
            return None

    except:
        return None
    entry["text"] = wikitext

    return json.dumps(entry, ensure_ascii=False)


def check_dir(path):
    dirname = os.path.abspath(os.path.dirname(path))
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def load_pages(args):
    xml_file_name = f"kowiki-{args.date}-pages-articles.xml"
    dump_xml_file = os.path.join(args.workspace, xml_file_name)
    with open(dump_xml_file) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    mediawiki = data_dict["mediawiki"]
    pages = mediawiki["page"]  # type(pages) == list
    if args.debug:
        pages = pages[:200]
    return pages


def main():
    parser = ArgumentParser()
    parser.add_argument("--date", type=str, required=True)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--save-base", type=str, default="../kowiki_data")
    args = parser.parse_args()
    args.multiline_pattern = re.compile("\\n{3,}")
    workspace = os.path.join(args.save_base, args.date, "workspace")
    os.makedirs(workspace, exist_ok=True)
    text_dir = os.path.join(workspace, "texts")
    os.makedirs(text_dir, exist_ok=True)
    args.workspace = workspace
    args.text_dir = text_dir

    print("Parsing Pages", flush=True)
    pages = load_pages(args)
    # n_workers = mp.cpu_count() // 2
    n_workers = mp.cpu_count() - 8
    pool = mp.Pool(n_workers)
    print("Transforming Pages to Wikitext", flush=True)
    total = len(pages)
    async_entries = pool.imap(
        transform_page_to_wikitext, pages, chunksize=n_workers * 64
    )

    save_path = os.path.join(args.workspace, "kowikitext.json")
    print(f"Saving to {save_path}", flush=True)
    async_iterator = tqdm(async_entries, total=total)
    num_articles = 0
    with open(save_path, "w") as f:
        for entry in async_iterator:
            if entry is None:
                continue
            f.write(entry)
            f.write("\n")
            num_articles += 1
    pool.close()
    pool.join()

    entry = {
        "date": args.date,
        "save_path": save_path,
        "workspace": workspace,
        "articles": num_articles,
    }
    metadata_path = os.path.join(workspace, "metadata.json")
    with open(metadata_path, "w") as f:
        f.write(json.dumps(entry, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
