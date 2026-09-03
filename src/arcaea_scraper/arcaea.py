import requests
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import ast
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
        self.all_scores_raw = None

    def _get(self, url):
        try:
            result = requests.get(url=url, cookies=self.cookie)
            result.raise_for_status()
            print("Done, waiting for 2 seconds")
            time.sleep(2)
            return result.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed: {e}")

    def save_scores(self, difficulties=None):
        try:
            self.all_scores_raw = pd.read_csv(f"{self.data_dir}/all.csv")
            print("Cached scores found. Pick an option:")
            print("[1] Start from scratch", "[2] Do nothing", "Your choice: ", sep="\n")
            choice = input()
            match choice:
                case 1:
                    Path.unlink(self.data_dir / "all.csv")
                    Path.unlink(self.data_dir / "all_clean.csv")
                    self._all_scores_clean(difficulties)
                case _:
                    return
        except FileNotFoundError:
            print("No cached scores found. Starting from scratch.")

    def _all_scores_get(self, difficulties=None):
        try:
            self.all_scores_raw = pd.read_csv(f"{self.data_dir}/all.csv")

        except FileNotFoundError:
            print("No cached scores found. Starting from scratch.")

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
                response = self._get(url)
                charts = pd.DataFrame(response["value"]["scores"])
                chart_count = response["value"]["count"]
                if chart_count % 10 == 0:
                    last_page = chart_count
                else:
                    last_page = chart_count // 10 + 1
                if self.all_scores_raw is None:
                    self.all_scores_raw = charts
                else:
                    self.all_scores_raw = pd.concat(
                        [self.all_scores_raw, charts], ignore_index=True
                    )
                page += 1
                first = False
            print(f"Difficulty {difficulty} done! Moving on.")

        print("All difficulties done. Writing to all.csv")
        self.all_scores_raw.to_csv(f"{self.data_dir}/all.csv", index=False)
        print("Done. Moving on to cleaning.")
        self._all_scores_clean()
        print("Done!")

    def _all_scores_clean(self):
        raw_data = pd.read_csv(test.data_dir / "all.csv")
        columns_to_keep = ["title", "difficulty", "score", "difficulty_alias"]
        data = raw_data[columns_to_keep]
        data["title"] = data["title"].apply(ast.literal_eval)
        lang = pd.json_normalize(data["title"])
        data["title"] = lang["en"]
        data["difficulty_alias"] = data["difficulty_alias"].fillna(-1)
        data["difficulty"] = data["difficulty"].map(
            {0: "PST", 1: "PRS", 2: "FTR", 3: "BYD", 4: "ETR"}
        )
        temp = data["difficulty_alias"] == 1
        data.loc[temp, "difficulty"] = "INS"
        self.all_scores_cleaned = data.drop("difficulty_alias", axis="columns")
        self.all_scores_cleared.to.csv(f"{self.data_dir}/all_clean.csv")


if __name__ == "__main__":
    pass
