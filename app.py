from flask import Flask, render_template
import pandas as pd
from pathlib import Path

app = Flask(__name__)

EXPORTS_FOLDER = Path("exports")

def get_latest_excel():
    files = list(EXPORTS_FOLDER.glob("*.xlsx")) + list(EXPORTS_FOLDER.glob("*.xls"))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

@app.route("/")
def dashboard():
    latest_file = get_latest_excel()

    if latest_file is None:
        return render_template(
            "index.html",
            no_file=True,
            latest_file="No Excel file found",
            total_tickets=0,
            active_tickets=0,
            stuck_count=0,
            avg_days=0,
            status_summary=[],
            tickets=[]
        )

    df = pd.read_excel(latest_file)

    # Clean column names just in case there are spaces
    df.columns = [str(c).strip() for c in df.columns]

    total_tickets = len(df)

    status_col = "Job Status"
    days_col = "Days In Status"
    assigned_col = "Assigned To"
    number_col = "Job Number"

    active_tickets = len(df[df[status_col].notna()]) if status_col in df.columns else total_tickets

    if days_col in df.columns:
        df[days_col] = pd.to_numeric(df[days_col], errors="coerce").fillna(0)
        stuck = df[df[days_col] >= 3]
        avg_days = round(df[days_col].mean(), 2)
    else:
        stuck = pd.DataFrame()
        avg_days = 0

    if status_col in df.columns:
        status_summary = (
            df.groupby(status_col)
            .size()
            .reset_index(name="Count")
            .sort_values("Count", ascending=False)
        )
    else:
        status_summary = pd.DataFrame(columns=[status_col, "Count"])

    keep_cols = [c for c in [number_col, status_col, days_col, assigned_col, "Customer", "Start Date", "Modified Date"] if c in df.columns]
    tickets = df[keep_cols].to_dict(orient="records") if keep_cols else df.to_dict(orient="records")

    return render_template(
        "index.html",
        no_file=False,
        latest_file=latest_file.name,
        total_tickets=total_tickets,
        active_tickets=active_tickets,
        stuck_count=len(stuck),
        avg_days=avg_days,
        status_summary=status_summary.to_dict(orient="records"),
        tickets=tickets
    )

if __name__ == "__main__":
    app.run(debug=True)