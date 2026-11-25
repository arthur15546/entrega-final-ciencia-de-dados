from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "dados"
OUTPUT_DIR = Path(__file__).resolve().parent / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def read_jsonl(filename: str) -> pd.DataFrame:
    return pd.read_json(DATA_DIR / filename, lines=True)


weekly = read_jsonl("weekly_performance.jsonl")
hotels = read_jsonl("hotels.jsonl")
rates = read_jsonl("rate_decisions.jsonl")
reviews = read_jsonl("reviews.jsonl")
scenarios = read_jsonl("review_scenarios.jsonl")

weekly["week_start"] = pd.to_datetime(weekly["week_start"])
weekly["month"] = weekly["week_start"].dt.to_period("M").astype(str)
weekly["year"] = weekly["week_start"].dt.year

monthly_rows = []
for (hotel_id, month), group in weekly.groupby(["hotel_id", "month"], sort=True):
    available = group["available_rooms"].sum()
    sold = group["rooms_sold"].sum()
    room_revenue = group["room_revenue"].sum()
    total_revenue = group["total_revenue"].sum()
    review_count = group["review_count"].sum()
    mean_rating = (
        (group["mean_rating"].fillna(0) * group["review_count"].fillna(0)).sum()
        / review_count
        if review_count
        else None
    )
    monthly_rows.append(
        {
            "hotel_id": hotel_id,
            "hotel_name": group["hotel_name"].iloc[0],
            "tier": group["tier"].iloc[0],
            "month": month,
            "year": int(group["year"].iloc[0]),
            "available_rooms": available,
            "rooms_sold": sold,
            "occupancy": sold / available if available else None,
            "adr": room_revenue / sold if sold else None,
            "revpar": room_revenue / available if available else None,
            "trevpar": total_revenue / available if available else None,
            "mean_rating": mean_rating,
            "review_count": review_count,
            "event_nights": group["event_nights"].sum(),
        }
    )

monthly = pd.DataFrame(monthly_rows)
monthly.to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False)

hotel_rows = []
for hotel_id, group in monthly.groupby("hotel_id"):
    available = group["available_rooms"].sum()
    sold = group["rooms_sold"].sum()
    review_count = group["review_count"].sum()
    hotel_rows.append(
        {
            "hotel_id": hotel_id,
            "hotel_name": group["hotel_name"].iloc[0],
            "tier": group["tier"].iloc[0],
            "available_rooms": available,
            "rooms_sold": sold,
            "occupancy": sold / available if available else None,
            "adr": (
                group["adr"].multiply(group["rooms_sold"]).sum() / sold
                if sold
                else None
            ),
            "revpar": (
                group["revpar"].multiply(group["available_rooms"]).sum() / available
                if available
                else None
            ),
            "trevpar": (
                group["trevpar"].multiply(group["available_rooms"]).sum() / available
                if available
                else None
            ),
            "mean_rating": (
                group["mean_rating"].multiply(group["review_count"]).sum()
                / review_count
                if review_count
                else None
            ),
            "review_count": review_count,
        }
    )

hotel_summary = pd.DataFrame(hotel_rows)

weekly["weighted_ari"] = weekly["ari"] * weekly["available_rooms"]
weekly["weighted_mpi"] = weekly["mpi"] * weekly["available_rooms"]
weekly["weighted_rgi"] = weekly["rgi"] * weekly["available_rooms"]
competition = (
    weekly.groupby(["hotel_id", "hotel_name", "tier"], as_index=False)
    .agg(
        ari=("weighted_ari", lambda s: s.sum()),
        mpi=("weighted_mpi", lambda s: s.sum()),
        rgi=("weighted_rgi", lambda s: s.sum()),
        available=("available_rooms", "sum"),
    )
)
competition["ari"] = competition["ari"] / competition["available"]
competition["mpi"] = competition["mpi"] / competition["available"]
competition["rgi"] = competition["rgi"] / competition["available"]
hotel_summary = hotel_summary.merge(
    competition.drop(columns="available"), on=["hotel_id", "hotel_name", "tier"], how="left"
)
hotel_summary.to_csv(OUTPUT_DIR / "hotel_summary.csv", index=False)

competition_year_rows = []
for (year, hotel_id), group in weekly.groupby(
    [weekly["week_start"].dt.year, "hotel_id"], sort=True
):
    available = group["available_rooms"].sum()
    row = hotels.loc[hotels["hotel_id"].eq(hotel_id)].iloc[0]
    competition_year_rows.append(
        {
            "year": int(year),
            "hotel_id": hotel_id,
            "hotel_name": row["name"],
            "tier": row["tier"],
            "ari": (group["ari"] * group["available_rooms"]).sum() / available,
            "mpi": (group["mpi"] * group["available_rooms"]).sum() / available,
            "rgi": (group["rgi"] * group["available_rooms"]).sum() / available,
            "revpar": group["room_revenue"].sum() / available,
        }
    )
pd.DataFrame(competition_year_rows).to_csv(
    OUTPUT_DIR / "competitive_year_summary.csv", index=False
)

reviews["review_date"] = pd.to_datetime(reviews["review_date"])
reviews["year"] = reviews["review_date"].dt.year
reviews = reviews.merge(
    hotels[["hotel_id", "hotel_name", "tier"]] if "hotel_name" in hotels else
    hotels.rename(columns={"name": "hotel_name"})[["hotel_id", "hotel_name", "tier"]],
    on="hotel_id",
    how="left",
)

scenario_counts = (
    reviews.groupby(["year", "hotel_id", "hotel_name", "tier", "scenario_id"])
    .size()
    .rename("review_count")
    .reset_index()
    .merge(scenarios, on="scenario_id", how="right")
)
scenario_counts["review_count"] = scenario_counts["review_count"].fillna(0).astype(int)
scenario_counts["observed_share"] = (
    scenario_counts["review_count"] / scenario_counts["review_count"].sum()
)
scenario_counts.to_csv(OUTPUT_DIR / "scenario_summary.csv", index=False)

print("Dados resumidos gerados em", OUTPUT_DIR)
