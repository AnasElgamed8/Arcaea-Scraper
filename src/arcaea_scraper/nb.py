import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _(tadata):
    import pandas as pd
    import marimo as mo
    from pathlib import Path
    import ast
    from Arcaea import Arcaea

    test = Arcaea()
    tadata
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
