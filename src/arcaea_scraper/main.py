import requests
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import os
import time


class Arcaea:
    def __init__(self):
        self.work_dir = Path(__file__).resolve().parent.parent.parent
        self.data_dir = self.work_dir / "data"
        load_dotenv()
        self.cookie = {"ctrcode": ";", "sid": os.getenv("COOKIE")}
        self.base_url = """https://webapi.lowiro.com/webapi"""
        self.b50_url = f"""{self.base_url}/score/rating/me"""
        self.songs_url = f"""{self.base_url}/score/song/me/all?difficulty="""
        self.all_scores = None

    def get(self, url):
        try:
            result = requests.get(url=url, cookies=self.cookie)
            result.raise_for_status()
            print("Done, waiting for 2 seconds")
            print(0)
            time.sleep(1)
            print(1)
            print.sleep(1)
            print(2)
            return result.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed: {e}")

    def all_scores_get(self, difficulties=None):
        if difficulties is None:
            difficulties = [0, 1, 2, 3, 4]
        for difficulty in difficulties:
            page = 1
            last_page = 1
            first = True
            while page <= last_page:
                if not first:
                    print(
                        f"Difficulty {difficulty} - page {page}. ~{last_page - page} pages left"
                    )
                else:
                    print(f"Starting difficulty {difficulty}. First Page")
                url = f"{self.songs_url}{difficulty}&page={page}&sort=title"
                response = self.get(url)
                charts = pd.DataFrame(response["value"]["scores"])
                chart_count = response["value"]["count"]
                if chart_count % 10 == 0:
                    last_page = chart_count
                else:
                    last_page = chart_count // 10 + 1
                if self.all_scores is None:
                    self.all_scores = charts
                else:
                    self.all_scores = pd.concat(
                        [self.all_scores, charts], ignore_index=True
                    )
                page += 1
                first = False
            print(f"Difficulty {difficulty} done! Moving on.")

        self.all_scores.to_csv(f"{self.data_dir}/all.csv", index=False)


if __name__ == "__main__":
    test = Arcaea()
    test.all_scores_get()
    print("done")
