import transformers
import datasets
from argparse import ArgumentParser
import os
from slack_sdk import WebClient


def gen_function(args):
    save_dir = os.path.join(args.save_base, args.date)
    train_path = os.path.join(save_dir, "workspace", "kowikitext.json")
    # valid_path = os.path.join(save_dir, "kowikitext_valid.json")
    # test_path = os.path.join(save_dir, "kowikitext_test.json")

    write_token = os.environ.get("HF_WRITE_TOKEN")
    print("Loading datasets", flush=True)

    # valid_dataset = datasets.load_dataset("json", data_files=valid_path, split="train")
    # test_dataset = datasets.load_dataset("json", data_files=test_path, split="train")
    train_dataset = datasets.load_dataset("json", data_files=train_path, split="train")
    # all_dataset = {"train": train_dataset, "valid": valid_dataset, "test": test_dataset}
    # all_dataset = datasets.DatasetDict(all_dataset)

    print("Loaded datasets", flush=True)

    # push
    version = transformers.__version__
    dataset_version = args.date

    # res = all_dataset.push_to_hub(
    #     repo_id=args.repo,
    #     commit_message=f"Upload dump {args.date}",
    #     private=True,
    #     token=write_token,
    #     revision=f"{args.date}",
    # )

    train_dataset.push_to_hub(
        repo_id=args.repo,
        commit_message=f"Upload dump {args.date}",
        private=True,
        token=write_token,
        revision=f"{args.date}",
        split="train",
    )
    # valid_dataset.push_to_hub(
    #     repo_id=args.repo,
    #     commit_message=f"Upload dump {args.date}",
    #     private=True,
    #     token=write_token,
    #     revision=f"{args.date}",
    #     split="valid",
    # )
    # test_dataset.push_to_hub(
    #     repo_id=args.repo,
    #     commit_message=f"Upload dump {args.date}",
    #     private=True,
    #     token=write_token,
    #     revision=f"{args.date}",
    #     split="test",
    # )
    print("Pushed to Hub")


def setup_slack_client():
    SLACK_BOT_TOKEN = os.environ["MONITORING_SLACK_BOT_TOKEN"]
    return WebClient(token=SLACK_BOT_TOKEN)


def post_slack_message(client, text, channel="erc-cluster-monitoring"):
    client.chat_postMessage(channel=channel, text=text)


def main():
    parser = ArgumentParser()
    parser.add_argument("--date", type=str, required=True)
    parser.add_argument("--repo", type=str, default="chanwoopark/kowikitext")
    parser.add_argument("--save-base", type=str, default="../kowiki_data")

    args = parser.parse_args()
    print("Starting...")
    gen_function(args)
    client = setup_slack_client()
    post_slack_message(client, f"Uploaded {args.date} to Hub")


if __name__ == "__main__":
    main()
