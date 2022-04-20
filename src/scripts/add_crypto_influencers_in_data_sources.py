"""Module for adding crypto influencers in twitter data sources."""
from agblox.settings import DATALAKE_API_PASSWORD, DATALAKE_API_URL, DATALAKE_API_USER
import pandas as pd
import requests


def username_cleaner(username: str) -> str:
    """Function will clean the twitter handle."""
    if username.find("@") == 0:
        username = username[1:]
    if username.find("://"):
        username = username.split("/")[-1]
        if username.find("?") >= 0:
            username = username.split("?")[0]
        if username.find("?lang=en") >= 0:
            username = username.split("?lang=en")[0]

    return username


if __name__ == "__main__":
    google_sheet_url = (
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vTUOriIw913AQWxkZ9vI3x30upUwM8p1"
        "s6G6M6oms9R_TSG_EI--N1OE_ilrqRUk_OSrKJh8adCKJpI/pub?gid=0&single=true&output=csv"
    )
    google_sheet = pd.read_csv(google_sheet_url)
    google_sheet = google_sheet.fillna("")

    ENDPOINT = f"{DATALAKE_API_URL}/sources/twitter"
    for _index, profile in google_sheet.iterrows():
        twitter_handle = username_cleaner(profile["twitter"])
        if twitter_handle == "":
            continue
        data = {"name": twitter_handle, "tags": ["crypto", profile["assetName"]]}
        response = requests.post(
            url=ENDPOINT,
            auth=requests.auth.HTTPBasicAuth(DATALAKE_API_USER, DATALAKE_API_PASSWORD),
            json=data,
        )
        if response.status_code != 409:
            print("Index no. ", _index)
            print("Error Code. ", response.status_code)
            print(data)
            print(response.content)
            print("------------------")
