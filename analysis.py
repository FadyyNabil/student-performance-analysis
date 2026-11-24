"""Explore student grades with pandas. Run this file or use analysis.ipynb."""
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

import matplotlib.pyplot as plt
import pandas as pd

DATA_URL = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
STUDY_LABELS = {1: "<2 hours", 2: "2-5 hours", 3: "5-10 hours", 4: ">10 hours"}


def load_data(folder):
    """Use the included CSV, or download only the math file from UCI."""
    path = folder / "student-mat.csv"
    if not path.exists():
        with urlopen(DATA_URL, timeout=30) as response:
            archive = ZipFile(BytesIO(response.read()))
        # UCI's download currently contains another ZIP with the CSV inside.
        if "student.zip" in archive.namelist():
            archive = ZipFile(BytesIO(archive.read("student.zip")))
        path.write_bytes(archive.read("student-mat.csv"))
    return pd.read_csv(path, sep=";")


def check_data(df):
    """Stop rather than silently calculate with missing or invalid key data."""
    required = {"studytime", "failures", "G3"}
    if df.empty or not required.issubset(df.columns):
        raise ValueError("Expected nonempty UCI math data with studytime, failures and G3.")
    if df[list(required)].isna().any().any():
        raise ValueError("Missing values in the analysis columns. Inspect the CSV first.")
    if not df["studytime"].isin([1, 2, 3, 4]).all():
        raise ValueError("Unexpected study-time category.")
    if not df["G3"].between(0, 20).all() or not df["failures"].between(0, 4).all():
        raise ValueError("Grade or past-failure values outside the source's range.")
    # Report duplicates, but do not delete them: identical rows can be different students.
    print(f"Rows: {len(df)} | Columns: {len(df.columns)}")
    print(f"Missing cells: {df.isna().sum().sum()} | Full duplicate rows: {df.duplicated().sum()}")


def summarize(df):
    """Group by study time and by whether any past class failure was recorded."""
    study = df.groupby("studytime")["G3"].agg(students="size", average_grade="mean")
    study = study.reindex([1, 2, 3, 4])
    study.index = study.index.map(STUDY_LABELS)
    study.index.name = "weekly_study_time"

    work = df.assign(past_failure=df["failures"].gt(0))
    failures = work.groupby("past_failure")["G3"].agg(students="size", average_grade="mean")
    failures.index = failures.index.map({False: "No past failure", True: "Any past failure"})
    return study, failures


def plot_study_time(study, path):
    """Keep a zero baseline and show group sizes so the comparison is not misleading."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.bar(study.index, study["average_grade"], color="#247C83", width=0.62)
    ax.set_ylim(0, 20)
    ax.set_ylabel("Average final math grade (0-20)")
    ax.set_xlabel("Reported weekly study time")
    ax.set_title("Study time and final math grades", loc="left", fontsize=17, pad=24)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=0.18)
    for bar, (_, row) in zip(bars, study.iterrows()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.35,
                f"{row['average_grade']:.2f}\nn={int(row['students'])}",
                ha="center", va="bottom", fontsize=11)
    fig.text(0.1, 0.035, "Source: UCI Student Performance, math sample (395 records). Association is not causation.",
             fontsize=9, color="#444444")
    fig.tight_layout(rect=[0.02, 0.07, 0.99, 1])
    fig.savefig(path, dpi=160, facecolor="white")
    return fig


def main():
    folder = Path(__file__).resolve().parent
    df = load_data(folder)
    check_data(df)
    study, failures = summarize(df)
    print("\nStudy-time groups:\n", study.round(2).to_string())
    print("\nPast-failure groups:\n", failures.round(2).to_string())
    study.to_csv(folder / "study_summary.csv", float_format="%.4f")
    failures.to_csv(folder / "failure_summary.csv", float_format="%.4f")
    fig = plot_study_time(study, folder / "study_time.png")
    plt.close(fig)
    print("\nSaved study_summary.csv, failure_summary.csv and study_time.png")


if __name__ == "__main__":
    main()
