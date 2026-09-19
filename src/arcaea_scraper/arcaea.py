import requests
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
import ast
import os
import time


class Arcaea:
    def __init__(self):

        # Load dirs
        self.work_dir = Path(__file__).resolve().parent.parent.parent
        self.data_dir = self.work_dir / "data"

        self._raw_scores_dir = Path(f"{self.data_dir}/all.csv")
        self._clean_scores_dir = Path(f"{self.data_dir}/all_clean.csv")

        # Cookie Handling
        load_dotenv()
        self._cookie = {"ctrcode": ";", "sid": os.getenv("COOKIE")}

        # Endpoints
        self._base_url = """https://webapi.lowiro.com/webapi"""
        self._b50_url = f"""{self._base_url}/score/rating/me"""
        self._songs_url = f"""{self._base_url}/score/song/me/all?difficulty="""

        # is this needed?
        self.all_scores_raw = pd.DataFrame()

    # Main score savaing function
    def save_scores(self, difficulties=None):
        try:
            # Existing scores check
            self.all_scores_raw = pd.read_csv(self._raw_scores_dir)
            print("Cached scores found. Pick an option:")
            print(
                "[1] Start from scratch",
                "[2] Clean the dataset only",
                "[3] just load the sheets (default)",
                "Your choice: ",
                sep="\n",
            )
            choice = int(input())

            match choice:
                case 1:
                    Path.unlink(self._raw_scores_dir)
                    Path.unlink(self._clean_scores_dir, missing_ok=True)
                    self._all_scores_get(difficulties)
                    self._all_scores_clean()
                case 2:
                    Path.unlink(self._clean_scores_dir, missing_ok=True)
                    self._all_scores_clean()

                case _:
                    self._all_scores_cleaned = pd.read_csv(self._clean_scores_dir)
                    return

        except FileNotFoundError:
            print("No cached scores found. Starting from scratch.")
            self._all_scores_get(difficulties)

    # Web requests function
    def _get(self, url) -> dict:
        try:
            # Make a request then wait for 2 seconds
            result = requests.get(url=url, cookies=self._cookie)

            result.raise_for_status()
            print("Done, waiting for 2 seconds")
            time.sleep(2)

            return result.json()

        except requests.exceptions.RequestException as e:
            print(f"Failed: {e}")

    def _all_scores_get(self, difficulties=None):
        # get all difficulties by default
        if difficulties is None:
            difficulties = [0, 1, 2, 3, 4]

        # Difficulties loop
        for difficulty in difficulties:
            page = 1
            last_page = 1
            first = True

            # Pages loop
            while page <= last_page:
                if not first:
                    print(
                        f"Difficulty {difficulty} - page {page}. ~{last_page - page} pages left"
                    )

                else:
                    print(f"Starting difficulty {difficulty}. First Page")

                # Make the request by page and difficulty
                url = f"{self._songs_url}{difficulty}&page={page}&sort=title"
                response = self._get(url)

                # Save only the useful columns
                charts = pd.DataFrame(response["value"]["scores"])

                # Calculate the last page given the note count on the first run for each difficulty
                if first:
                    chart_count = response["value"]["count"]
                    if chart_count % 10 == 0:
                        last_page = chart_count // 10
                    else:
                        last_page = chart_count // 10 + 1

                # I don't think this is needed
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
        self.all_scores_raw.to_csv(self._raw_scores_dir, index=False)

        print("Fetching scores done!")

    def _all_scores_clean(self):
        # read raw scores from disk
        self.all_scores_raw = pd.read_csv(self._raw_scores_dir)

        # Keep only useful columns
        columns_to_keep = ["title", "difficulty", "score", "difficulty_alias"]
        data = self.all_scores_raw[columns_to_keep]

        # keep only english titles
        data["title"] = data["title"].apply(ast.literal_eval)
        lang = pd.json_normalize(data["title"])
        data["Title"] = lang["en"]

        # Map the main 5 difficulties
        data["Difficulty"] = data["difficulty"].map(
            {0: "PST", 1: "PRS", 2: "FTR", 3: "BYD", 4: "ETR"}
        )

        # handle INS difficulty
        data["difficulty_alias"] = data["difficulty_alias"].fillna(-1)
        temp = data["difficulty_alias"] == 1
        data.loc[temp, "Difficulty"] = "INS"

        # clean column names
        data["Score"] = data["score"]
        columns_to_keep = ["Title", "Difficulty", "Score"]
        self._all_scores_cleaned = data[columns_to_keep]

        # save to disk
        self._all_scores_cleaned.to_csv(self._clean_scores_dir, index=False)
        print("Cleaning done!")


if __name__ == "__main__":
    test = Arcaea()
    test.save_scores()
