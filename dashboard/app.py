from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent / "data"

st.set_page_config(
    page_title="Painel Gerencial de Hotel",
    page_icon="",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
    [data-testid="stMetric"] {
        background: #f4f7fb;
        border: 1px solid #dde5ef;
        border-radius: 10px;
        padding: 14px;
    }
    .decision-box {
        background: #eef5ff;
        border-left: 4px solid #1f77b4;
        padding: 10px 14px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    monthly = pd.read_csv(DATA_DIR / "monthly_summary.csv")
    hotels = pd.read_csv(DATA_DIR / "hotel_summary.csv")
    scenarios = pd.read_csv(DATA_DIR / "scenario_summary.csv")
    competitive_year = pd.read_csv(DATA_DIR / "competitive_year_summary.csv")
    monthly["month"] = pd.PeriodIndex(monthly["month"], freq="M").to_timestamp()
    return monthly, hotels, scenarios, competitive_year


monthly, hotel_summary, scenario_summary, competitive_year = load_data()

st.title("Painel Gerencial de Hotel")
st.caption(
    "Decisões apoiadas por desempenho mensal, posicionamento competitivo e avaliações."
)

st.markdown(
    """
    <div class="decision-box">
    <b>Público:</b> gerente geral de hotel &nbsp;|&nbsp;
    <b>Decisões:</b> ajustar preço e ocupação; priorizar melhorias operacionais; comparar posição no mercado.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Filtros")
    tier = st.selectbox(
        "Tier",
        ["Todos"] + sorted(monthly["tier"].dropna().unique().tolist()),
    )
    year = st.selectbox(
        "Ano",
        ["Todos"] + sorted(monthly["year"].unique().tolist()),
    )
    hotel_options = ["Todos"] + sorted(
        monthly.loc[
            monthly["tier"].eq(tier) if tier != "Todos" else pd.Series(True, index=monthly.index),
            "hotel_name",
        ].unique()
        .tolist()
    )
    hotel = st.selectbox("Hotel", hotel_options)

filtered = monthly.copy()
hotel_filtered = hotel_summary.copy()
competition_filtered = competitive_year.copy()
scenario_filtered = scenario_summary.copy()

if tier != "Todos":
    filtered = filtered[filtered["tier"] == tier]
    hotel_filtered = hotel_filtered[hotel_filtered["tier"] == tier]
    competition_filtered = competition_filtered[
        competition_filtered["tier"] == tier
    ]
    scenario_filtered = scenario_filtered[
        scenario_filtered["tier"] == tier
    ]
if year != "Todos":
    filtered = filtered[filtered["year"] == year]
    competition_filtered = competition_filtered[
        competition_filtered["year"] == year
    ]
    scenario_filtered = scenario_filtered[
        scenario_filtered["year"] == year
    ]
if hotel != "Todos":
    filtered = filtered[filtered["hotel_name"] == hotel]
    hotel_filtered = hotel_filtered[hotel_filtered["hotel_name"] == hotel]
    competition_filtered = competition_filtered[
        competition_filtered["hotel_name"] == hotel
    ]
    scenario_filtered = scenario_filtered[
        scenario_filtered["hotel_name"] == hotel
    ]

if filtered.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    available = filtered["available_rooms"].sum()
    sold = filtered["rooms_sold"].sum()
    room_revenue = (
        filtered["adr"].fillna(0) * filtered["rooms_sold"]
    ).sum()
    total_revenue = (
        filtered["trevpar"].fillna(0) * filtered["available_rooms"]
    ).sum()
    review_count = filtered["review_count"].sum()
    mean_rating = (
        filtered["mean_rating"].fillna(0) * filtered["review_count"]
    ).sum()
    mean_rating = mean_rating / review_count if review_count else None

    occupancy = sold / available if available else None
    adr = room_revenue / sold if sold else None
    revpar = room_revenue / available if available else None

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Ocupação", f"{occupancy:.1%}" if occupancy is not None else "N/D")
    k2.metric("ADR", f"{adr:,.2f}" if adr is not None else "N/D")
    k3.metric("RevPAR", f"{revpar:,.2f}" if revpar is not None else "N/D")
    k4.metric(
        "Nota média",
        f"{mean_rating:.2f}" if mean_rating is not None else "N/D",
    )

    st.subheader("Evolução mensal")
    line_data = (
        filtered.groupby("month", as_index=False)
        .agg(
            available_rooms=("available_rooms", "sum"),
            rooms_sold=("rooms_sold", "sum"),
            room_revenue=("adr", lambda s: 0),
        )
    )
    monthly_detail = (
        filtered.groupby("month", as_index=False)
        .apply(
            lambda g: pd.Series(
                {
                    "occupancy": g["rooms_sold"].sum()
                    / g["available_rooms"].sum(),
                    "adr": (
                        g["adr"].multiply(g["rooms_sold"]).sum()
                        / g["rooms_sold"].sum()
                        if g["rooms_sold"].sum()
                        else None
                    ),
                }
            ),
            include_groups=False,
        )
        .reset_index(drop=True)
    )

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly_detail["month"],
            y=monthly_detail["occupancy"] * 100,
            name="Ocupação",
            mode="lines+markers",
            line={"color": "#1f77b4", "width": 3},
        )
    )
    fig.add_trace(
        go.Scatter(
            x=monthly_detail["month"],
            y=monthly_detail["adr"],
            name="ADR",
            mode="lines+markers",
            yaxis="y2",
            line={"color": "#e67e22", "width": 3},
        )
    )
    fig.update_layout(
        title="Ocupação e ADR evoluem em escalas próprias",
        xaxis_title="Mês",
        yaxis={"title": "Ocupação (%)", "ticksuffix": "%"},
        yaxis2={
            "title": "ADR",
            "overlaying": "y",
            "side": "right",
        },
        legend={"orientation": "h", "y": 1.12},
        hovermode="x unified",
        height=390,
    )
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns((1.05, 1))

    with left:
        tier_data = filtered.groupby("tier", as_index=False).apply(
            lambda g: pd.Series(
                {
                    "Ocupação": g["rooms_sold"].sum()
                    / g["available_rooms"].sum()
                    * 100,
                    "ADR": g["adr"].multiply(g["rooms_sold"]).sum()
                    / g["rooms_sold"].sum(),
                    "RevPAR": g["room_revenue"].sum()
                    / g["available_rooms"].sum()
                    if "room_revenue" in g
                    else g["adr"].multiply(g["rooms_sold"]).sum()
                    / g["available_rooms"].sum(),
                }
            ),
            include_groups=False,
        ).reset_index(drop=True)
        tier_fig = px.bar(
            tier_data,
            x="tier",
            y="Ocupação",
            title="Ocupação média por tier",
            labels={"tier": "Tier", "Ocupação": "Ocupação (%)"},
            text="Ocupação",
            color="tier",
        )
        tier_fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        tier_fig.update_layout(showlegend=False, yaxis_ticksuffix="%", height=370)
        st.plotly_chart(tier_fig, use_container_width=True)

    with right:
        if competition_filtered.empty:
            st.info("Sem dados competitivos para o filtro atual.")
        else:
            scatter = px.scatter(
                competition_filtered,
                x="ari",
                y="mpi",
                size="revpar",
                color="tier",
                hover_name="hotel_name",
                hover_data={
                    "tier": True,
                    "ari": ":.1f",
                    "mpi": ":.1f",
                    "rgi": ":.1f",
                    "revpar": ":,.2f",
                },
                title="Posicionamento competitivo dos hotéis",
                labels={
                    "ari": "Índice de tarifa (ARI)",
                    "mpi": "Índice de ocupação (MPI)",
                    "revpar": "RevPAR",
                },
            )
            scatter.add_hline(y=100, line_dash="dot", line_color="#777")
            scatter.add_vline(x=100, line_dash="dot", line_color="#777")
            scatter.update_layout(height=370)
            st.plotly_chart(scatter, use_container_width=True)

    st.subheader("Cenários das avaliações")
    if scenario_filtered.empty:
        st.info("Sem cenários de avaliação para os filtros selecionados.")
    else:
        scenario_aggregated = (
            scenario_filtered.groupby(
                ["scenario_id", "label", "expected_sentiment"],
                as_index=False,
            )["review_count"]
            .sum()
        )
        scenario_fig = px.bar(
            scenario_aggregated.sort_values("review_count", ascending=True),
            x="review_count",
            y="label",
            orientation="h",
            title="Volume observado por cenário",
            labels={"review_count": "Avaliações", "label": "Cenário"},
            color="expected_sentiment",
            color_discrete_map={
                "positive": "#2ca02c",
                "negative": "#d62728",
                "mixed": "#9467bd",
            },
        )
        scenario_fig.update_layout(height=430)
        st.plotly_chart(scenario_fig, use_container_width=True)

    st.subheader("Tabela resumo por hotel")
    table = hotel_filtered.copy()
    if not table.empty:
        display = table[
            [
                "hotel_name",
                "tier",
                "occupancy",
                "adr",
                "revpar",
                "trevpar",
                "mean_rating",
                "review_count",
            ]
        ].rename(
            columns={
                "hotel_name": "Hotel",
                "tier": "Tier",
                "occupancy": "Ocupação",
                "adr": "ADR",
                "revpar": "RevPAR",
                "trevpar": "TRevPAR",
                "mean_rating": "Nota média",
                "review_count": "Avaliações",
            }
        )
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Ocupação": st.column_config.ProgressColumn(
                    "Ocupação", format="%.1%%", min_value=0, max_value=1
                ),
                "ADR": st.column_config.NumberColumn("ADR", format="%.2f"),
                "RevPAR": st.column_config.NumberColumn("RevPAR", format="%.2f"),
                "TRevPAR": st.column_config.NumberColumn("TRevPAR", format="%.2f"),
                "Nota média": st.column_config.NumberColumn("Nota média", format="%.2f"),
                "Avaliações": st.column_config.NumberColumn("Avaliações", format="%d"),
            },
        )

st.divider()
st.caption(
    "Fonte dos dados: dados sintéticos do projeto (weekly_performance, hotels, "
    "rate_decisions e reviews). Agregação mensal por hotel; pesos por quartos "
    "disponíveis ou vendidos, conforme a métrica. Dataset sintético."
)
