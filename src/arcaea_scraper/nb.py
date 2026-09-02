import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
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
    df.to_html("B50.html")
    return (df,)


@app.cell
def _(df):
    df
    return


if __name__ == "__main__":
    app.run()
