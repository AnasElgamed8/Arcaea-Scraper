from arcaea import Arcaea
import pandas as pd

test = Arcaea()
test.save_scores()
clean = test._all_scores_cleaned
sheet = pd.read_csv(test.data_dir / "sheet.csv")

sheet = sheet.drop(columns=["Score"])
sheet["merge_title"] = sheet["Title"].str.strip().str.lower()
clean["merge_title"] = clean["Title"].str.strip().str.lower()

final = pd.merge(
    left=sheet,
    right=clean[["merge_title", "Difficulty", "Score"]],
    on=["merge_title", "Difficulty"],
    how="left",
)

final = final.drop(columns=["merge_title"])
final.to_csv(test.data_dir / "sheet2.csv", index=False)
