import requests
import pandas as pd
from dotenv import load_dotenv
import os

#
# load_dotenv()
# url = """https://webapi.lowiro.com/webapi/score/rating/me"""
# cookie = {"ctrcode": ";", "sid": os.getenv("COOKIE")}
# test = requests.get(url=url, cookies=cookie)
# idk = test.json()
# df = pd.DataFrame(idk["value"]["best_rated_scores"])
# df.to_csv("B50.csv", index=False)
df = pd.read_csv("B50.csv")
df.info()
print(df.shape, df.head(50), df.describe())
