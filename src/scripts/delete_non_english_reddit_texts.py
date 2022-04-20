"""Module to append DELETE tag in case of non english texts from datalake."""
from agblox.settings import DATALAKE_API_PASSWORD, DATALAKE_API_URL, DATALAKE_API_USER
from langdetect import detect
import requests
from requests.auth import HTTPBasicAuth


def append_delete_in_non_english_texts() -> None:
    """Function will append delete tag in case of non english texts."""
    endpoint = "/texts?tags=reddit&with_sentiment=false&limit=100&sort_order=desc&with_count=true"
    reddit = requests.get(
        url=f"{DATALAKE_API_URL}{endpoint}",
        auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
    )
    reddit_texts = reddit.json()
    non_english_ids = []
    non_english_words = 0
    for item in reddit_texts:
        if item["sentiment"] is None:
            item["sentiment"] = {}
        if detect(item["text"]) != "en":
            if "DELETE" not in item["tags"]:
                item["tags"].append("DELETE")
            non_english_ids.append(item["id"])
            non_english_words += 1
    print("No. of non english words", non_english_words)

    # Append delete tags list
    for i, index in enumerate(non_english_ids):
        response = requests.put(
            url=f"{DATALAKE_API_URL}/texts/{index}",
            auth=HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
            json=reddit_texts[i],
        )
        print(i)
        print(response.text)


if __name__ == "__main__":
    append_delete_in_non_english_texts()
