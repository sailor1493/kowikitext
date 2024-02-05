import numpy as np
import os
from glob import glob
from tqdm import tqdm
from argparse import ArgumentParser
import json


def routine(args):
    save_dir = os.path.join(args.save_base, args.date)
    args.save_dir = save_dir
    os.makedirs(save_dir, exist_ok=True)
    workspace_dir = os.path.join(save_dir, "workspace")
    os.makedirs(workspace_dir, exist_ok=True)
    args.workspace = workspace_dir

    metadata_path = os.path.join(workspace_dir, "metadata.json")
    metadata = json.loads(open(metadata_path).read())
    num_articles = metadata["articles"]

    print("Sampling from concatenated texts", flush=True)
    n_train = int(0.90 * num_articles)
    n_dev = int(0.05 * num_articles)
    n_test = int(0.05 * num_articles)
    np.random.seed(0)
    indices = np.random.permutation(num_articles)
    train_indices = set(indices[:n_train])
    dev_indices = set(indices[n_train : n_train + n_dev])
    test_indices = set(indices[n_train + n_dev :])

    train_path = os.path.join(save_dir, "kowikitext_train.json")
    valid_path = os.path.join(save_dir, "kowikitext_valid.json")
    test_path = os.path.join(save_dir, "kowikitext_test.json")
    src_path = os.path.join(workspace_dir, "kowikitext.json")

    with open(src_path, "r") as f, open(train_path, "w") as f_train, open(
        valid_path, "w"
    ) as f_valid, open(test_path, "w") as f_test:
        for i, line in tqdm(enumerate(f)):
            try:
                entry = json.loads(line)
                line = json.dumps(entry, ensure_ascii=False)
                if i in train_indices:
                    f_train.write(line)
                    f_train.write("\n")
                elif i in dev_indices:
                    f_valid.write(line)
                    f_valid.write("\n")
                elif i in test_indices:
                    f_test.write(line)
                    f_test.write("\n")
            except:
                pass


def main():
    parser = ArgumentParser()
    parser.add_argument("--date", type=str, required=True)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--save-base", type=str, default="../kowiki_data")

    args = parser.parse_args()
    routine(args)


if __name__ == "__main__":
    main()
