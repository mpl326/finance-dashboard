
import streamlit as st
import pandas as pd
import altair as alt

#page configuration
st.set_page_config(
    page_title = "Earnings Call Sentiment - Event Study Dashboard",
    layout = "wide"
)

@st.cache_data
def load_data():
  df = pd.read_csv("dashboard_event_study_data.csv", parse_dates = ["event_date"])
  sentiment_cols = [
      "mgmtremarks_sentiment_score",
      "qa_sentiment_score",
      "average_sentiment_score"
  ]
  car_cols = [c for c in df.columns if c.startswith("CAR_")]
  return df, sentiment_cols, car_cols
df, sentiment_cols, car_cols = load_data()

st.title("Earnings Call Sentiment & Event Study Dashboard")

st.markdown("""
This dashboard lets you explore how earnings call sentimentrelates to stock performance
using abnormal returns from your event study.
""")

st.sidebar.header("Filters")

tickers = sorted(df["ticker"].unique())
selected_ticker = st.sidebar.selectbox("Select Company (Ticker)", tickers)
ticker_df = df[df["ticker"] == selected_ticker]

min_date = ticker_df["event_date"].min()
max_date = ticker_df["event_date"].max()

start_date, end_date = st.sidebar.date_input(
   "Earnings Event Date Range",
   value=[min_date, max_date],
   min_value=min_date,
   max_value=max_date
)

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

filtered = ticker_df[
    ticker_df["event_date"].between(start_date, end_date)
].sort_values("event_date")

st.sidebar.write(f"Events in range: **{len(filtered)}**")

window_choice = st.sidebar.selectbox(
    "Select CAR Window",
    car_cols,
    format_func=lambda c: c.replace("CAR_", " ").replace("_", " ").title()
)


if filtered.empty:
  st.warnings("No events found for this ticker in the selected date range.")
  st.stop()

col1, col2 = st.columns(2)

with col1:
  st.subheader("Event-level Data")
  table_cols = ["event_date"] + sentiment_cols + car_cols
  st.dataframe(
      filtered[table_cols].reset_index(drop=True),
      use_container_width=True
  )


with col2:
  st.subheader("Summary Statistics")
  avg_sent = filtered["average_sentiment_score"].mean()
  avg_car = filtered[window_choice].mean()

  c1, c2 = st.columns(2)
  c1.metric("Avg Sentiment (1-10)", f"{avg_sent:.2f}")
  c2.metric(f"Avg {window_choice}", f"{avg_car:.4f}")


    # Correlation
if filtered["average_sentiment_score"].nunique() > 1:
    corr = filtered["average_sentiment_score"].corr(filtered[window_choice])
    st.write(f"Correlation between sentiment and `{window_choice}`: **{corr:.3f}**")
else:
    st.write("Correlation not meaningful (constant sentiment values).")


# ------------------------------------------------------------
# Visualization 1 — Scatter (Sentiment vs CAR)
# ------------------------------------------------------------
st.subheader("Sentiment vs Abnormal Return (CAR)")

scatter_data = filtered[[
    "event_date", 
    "average_sentiment_score", 
    window_choice
]].copy()

scatter_data["event_label"] = scatter_data["event_date"].dt.strftime("%Y-%m-%d")

scatter_plot = (
    alt.Chart(scatter_data)
    .mark_circle(size=80)
    .encode(
        x=alt.X("average_sentiment_score", title="Average Sentiment Score (1–10)"),
        y=alt.Y(window_choice, title=window_choice),
        tooltip=["event_label", "average_sentiment_score", window_choice],
        color="event_label"
    )
    .interactive()
)

st.altair_chart(scatter_plot, use_container_width=True)

# ------------------------------------------------------------
# Visualization 2 — Event-Study Windows
# ------------------------------------------------------------
st.subheader("Event Study Window Comparison")

car_long = filtered.melt(
    id_vars=["ticker", "event_date", "average_sentiment_score"],
    value_vars=car_cols,
    var_name="window",
    value_name="CAR"
)

car_long["window_clean"] = (
    car_long["window"]
    .str.replace("CAR_", "")
    .str.replace("_", " ")
    .str.title()
)

view_mode = st.radio(
    "Display:",
    ["Average Across Events", "Each Event Separately"],
    horizontal=True
)

if view_mode == "Average Across Events":
    avg_car = car_long.groupby("window_clean", as_index=False)["CAR"].mean()
    bar_chart = (
        alt.Chart(avg_car)
        .mark_bar()
        .encode(
            x=alt.X("window_clean", title="CAR Window"),
            y=alt.Y("CAR", title="Average CAR"),
            tooltip=["window_clean", "CAR"]
        )
    )
    st.altair_chart(bar_chart, use_container_width=True)

else:
    car_long["event_label"] = car_long["event_date"].dt.strftime("%Y-%m-%d")
    line_chart = (
        alt.Chart(car_long)
        .mark_line(point=True)
        .encode(
            x=alt.X("window_clean", title="CAR Window"),
            y=alt.Y("CAR", title="CAR"),
            color="event_label",
            tooltip=["event_label", "window_clean", "CAR"]
        )
        .interactive()
    )
    st.altair_chart(line_chart, use_container_width=True)
