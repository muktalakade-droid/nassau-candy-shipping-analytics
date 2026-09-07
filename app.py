import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# ============================================================
# INTERACTIVE CROSS-FILTERING
# ============================================================
if "clicked_region" not in st.session_state:
    st.session_state.clicked_region = None
if "clicked_state" not in st.session_state:
    st.session_state.clicked_state = None
if "clicked_ship_mode" not in st.session_state:
    st.session_state.clicked_ship_mode = None
if "clicked_route" not in st.session_state:
    st.session_state.clicked_route = None
if "clicked_order" not in st.session_state:
    st.session_state.clicked_order = None

def _get_selection(event):
    """Return first selected row/point safely, or None."""
    if event is None:
        return None
    try:
        rows = event.selection.rows
        if rows:
            return rows[0]
    except Exception:
        pass
    try:
        points = event.selection.points
        if points:
            return points[0]
    except Exception:
        pass
    return None

def _point_value(point, key, fallback=None):
    if not point:
        return fallback
    try:
        return point.get(key, fallback)
    except AttributeError:
        return fallback

# =========================
# LOAD DATA
# =========================

file_path = "Nassau Candy Distributor (2).csv"
df = pd.read_csv(file_path)
df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="mixed", dayfirst=True)
df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Region Route"] = "Factory → " + df["Region"].astype(str)
df["State Route"] = "Factory → " + df["State/Province"].astype(str)

# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Nassau Candy Shipping Analytics",
    page_icon="🍬",
    layout="wide"
)


# =========================
# PROFESIONAL DASHBOARD DESIGN
# =========================
st.markdown("""
<style>
:root {
    --navy: #102A43;
    --blue: #1F6FEB;
    --light-blue: #EAF2FF;
    --border: #D9E2EC;
    --text: #243B53;
    --muted: #627D98;
}

.block-container {
    padding: 1.0rem 1.4rem 1.5rem 1.4rem;
    max-width: 100%;
}

/* Main dashboard background */
[data-testid="stAppViewContainer"] {
    background: #F6F8FB;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102A43 0%, #163B5C 100%);
}
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] input {
    color: #102A43 !important;
}

/* Date input visibility */
section[data-testid="stSidebar"] div[data-baseweb="input"] input {
    color: #102A43 !important;
    -webkit-text-fill-color: #102A43 !important;
    background-color: #FFFFFF !important;
    opacity: 1 !important;   
}

section[data-testid="stSidebar"] div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
}

/* Hero */
.dashboard-hero {
    background: linear-gradient(105deg, #102A43 0%, #174A7E 55%, #1F6FEB 100%);
    padding: 18px 24px;
    border-radius: 16px;
    margin-bottom: 14px;
    box-shadow: 0 8px 24px rgba(16,42,67,.14);
}
.dashboard-hero h1 {
    color: white !important;
    font-size: 28px !important;
    margin: 0 !important;
    font-weight: 800 !important;
}
.dashboard-hero p {
    color: #D9EAFB;
    margin: 5px 0 0 0;
    font-size: 13px;
}

/* Section headers */
.section-title {
    display: flex;
    align-items: center;
    gap: 9px;
    background: white;
    border: 1px solid var(--border);
    border-left: 5px solid var(--blue);
    padding: 9px 14px;
    border-radius: 10px;
    margin: 14px 0 8px 0;
    box-shadow: 0 2px 8px rgba(16,42,67,.05);
}
.section-title span {
    color: var(--text);
    font-size: 17px;
    font-weight: 800;
}

/* KPI cards */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin: 8px 0 14px 0;
}
.kpi-card {
    background: white;
    padding: 12px 14px;
    min-height: 82px;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 3px 10px rgba(16,42,67,.06);
    border-top: 3px solid var(--blue);
    transition: transform .15s ease, box-shadow .15s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(16,42,67,.10);
}
.kpi-title {
    font-size: 11px;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: .3px;
}
.kpi-value {
    font-size: 22px;
    font-weight: 800;
    color: var(--navy);
    margin-top: 3px;
}
.kpi-subtitle {
    font-size: 10px;
    color: #829AB1;
    margin-top: 3px;
}

/* Streamlit chart/table containers */
div[data-testid="stPlotlyChart"], div[data-testid="stDataFrame"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 4px;
    box-shadow: 0 2px 9px rgba(16,42,67,.05);
}

/* Reduce default heading spacing */
h1, h2, h3 { color: var(--text) !important; }
h2 { font-size: 1.25rem !important; margin-top: .5rem !important; }
h3 { font-size: 1rem !important; margin-top: .4rem !important; }

@media (max-width: 900px) {
    .kpi-container { grid-template-columns: repeat(2, 1fr); }
}
</style>

<div class="dashboard-hero">
    <h1>🍬 Nassau Candy — Shipping Route Efficiency Analytics</h1>
    <p>Executive logistics dashboard • Route performance • Geographic bottlenecks • Ship mode analysis • Drill-down insights</p>
</div>
""", unsafe_allow_html=True)

# =========================
# FILTERS
# =========================

st.sidebar.header("Dashboard Filters")

# Date Range Filter
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

start_date = st.sidebar.date_input(
    "Start Date (YYYY/MM/DD)",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    format="YYYY/MM/DD"
)

end_date = st.sidebar.date_input(
    "End Date (YYYY/MM/DD)",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    format="YYYY/MM/DD"
)

if start_date > end_date:
    st.sidebar.error("Start Date cannot be after End Date")
    start_date = min_date
    end_date = max_date

filtered_df = df[
    (df["Order Date"].dt.date >= start_date) &
    (df["Order Date"].dt.date <= end_date)
].copy()

date_range = [start_date, end_date]

# Region Filter
region_options = sorted(df["Region"].dropna().unique())

region_options = ["All"] + region_options

selected_region = st.sidebar.selectbox(
    "Select Region",
    options=region_options
)

# State Filter
state_options = sorted(df["State/Province"].dropna().unique())

state_options = ["All"] + state_options

selected_state = st.sidebar.selectbox(
    "Select State",
    options=state_options
)

# Ship Mode Filter
ship_mode_options = sorted(df["Ship Mode"].dropna().unique())

ship_mode_options = ["All"] + ship_mode_options

selected_ship_mode = st.sidebar.selectbox(
    "Select Ship Mode",
    options=ship_mode_options
)

# Keep original data
base_df = df.copy()

# Lead-Time Threshold
min_lead = int(df["Lead Time"].min())
max_lead = int(df["Lead Time"].max())

lead_time_threshold = st.sidebar.slider(
    "Lead-Time Threshold (Days)",
    min_value=min_lead,
    max_value=max_lead,
    value=int(df["Lead Time"].median()),
    step=1
)

# Apply Filters
# A visual click acts as an additional cross-filter.
effective_region = st.session_state.clicked_region or selected_region
effective_state = st.session_state.clicked_state or selected_state
effective_ship_mode = st.session_state.clicked_ship_mode or selected_ship_mode

if len(date_range) == 2:
    start_date = date_range[0]
    end_date = date_range[1]
else:
    start_date = date_range[0]
    end_date = date_range[0]

filtered_df = base_df[
    (base_df["Order Date"].dt.date >= start_date) &
    (base_df["Order Date"].dt.date <= end_date) &
    ((effective_region == "All") | (base_df["Region"] == effective_region)) &
    ((effective_state == "All") | (base_df["State/Province"] == effective_state)) &
    ((effective_ship_mode == "All") | (base_df["Ship Mode"] == effective_ship_mode))
].copy()

# Delay Frequency
delay_count = base_df[
    (base_df["Order Date"].dt.date >= start_date) &
    (base_df["Order Date"].dt.date <= end_date) &
    ((effective_region == "All") | (base_df["Region"] == effective_region)) &
    ((effective_state == "All") | (base_df["State/Province"] == effective_state)) &
    ((effective_ship_mode == "All") | (base_df["Ship Mode"] == effective_ship_mode)) &
    (base_df["Lead Time"] > lead_time_threshold)
].shape[0]



total_shipments = base_df[
    (base_df["Order Date"].dt.date >= start_date) &
(base_df["Order Date"].dt.date <= end_date) &
    (effective_region == "All" or base_df["Region"] == effective_region) &
    (effective_state == "All" or base_df["State/Province"] == effective_state) &
    (effective_ship_mode == "All" or base_df["Ship Mode"] == effective_ship_mode)
].shape[0]

delay_frequency = (
    delay_count / total_shipments * 100
    if total_shipments > 0 else 0
)


# Use filtered data for dashboard
df = filtered_df
filtered_df["Shipping Lead Time"] = (
    filtered_df["Ship Date"] - filtered_df["Order Date"]
).dt.days

avg_lead_time = (filtered_df["Ship Date"] - filtered_df["Order Date"]).dt.days.mean()

# Route Efficiency Score

min_lead_time = (filtered_df["Ship Date"] - filtered_df["Order Date"]).dt.days.min()
max_lead_time = (filtered_df["Ship Date"] - filtered_df["Order Date"]).dt.days.max()

if max_lead_time > min_lead_time:
    route_efficiency_score = (
        100 * (1 - (
            avg_lead_time - min_lead_time
        ) / (max_lead_time - min_lead_time))
    )
else:
    route_efficiency_score = 100


# =========================
# TITLE
# =========================

st.title("🍬 Nassau Candy Shipping Analytics")
st.write("E-Commerce Shipping Efficiency Dashboard")

active_clicks = []
if st.session_state.clicked_region:
    active_clicks.append(f"Region: {st.session_state.clicked_region}")
if st.session_state.clicked_state:
    active_clicks.append(f"State: {st.session_state.clicked_state}")
if st.session_state.clicked_ship_mode:
    active_clicks.append(f"Ship Mode: {st.session_state.clicked_ship_mode}")
if active_clicks:
    st.info("Cross-filter active — " + " | ".join(active_clicks))
    if st.button("Clear Visual Selections", key="clear_visual_selections"):
        st.session_state.clicked_region = None
        st.session_state.clicked_state = None
        st.session_state.clicked_ship_mode = None
        st.session_state.clicked_route = None
        st.session_state.clicked_order = None
        st.rerun()

# =========================
# KPI DATA
# =========================

total_orders = base_df["Order ID"].nunique()
total_sales = base_df["Sales"].sum()
total_profit = base_df["Gross Profit"].sum()


# REQUIREMENT KPIs

# Shipping Lead Time
base_df["Shipping Lead Time"] = (
    base_df["Ship Date"] - base_df["Order Date"]
).dt.days

shipping_lead_time = (
    filtered_df["Ship Date"] - filtered_df["Order Date"]
).dt.days

# Average Lead Time
avg_lead_time = (
    filtered_df["Ship Date"] - filtered_df["Order Date"]
).dt.days.mean()

# Route Volume
route_volume = filtered_df.groupby("Region Route")["Order ID"].nunique()

# ==============================
# KPI CARDS (styled globally above)

st.html(f"""
<div class="kpi-container">

    <div class="kpi-card">
    <div class="kpi-title">Shipping Lead Time</div>
    <div class="kpi-value">{shipping_lead_time.median():.1f} Days</div>
    <div class="kpi-subtitle">Median shipping duration</div>
</div>

    <div class="kpi-card">
        <div class="kpi-title">Avg Lead Time</div>
        <div class="kpi-value">{avg_lead_time:.1f} Days</div>
        <div class="kpi-subtitle">Average shipping time</div>
    </div>

    <div class="kpi-card">
    <div class="kpi-title">Route Volume</div>
    <div class="kpi-value">{route_volume.max():,}</div>
    <div class="kpi-subtitle">Highest orders on a route</div>
</div>

    <div class="kpi-card">
        <div class="kpi-title">Delay Frequency</div>
        <div class="kpi-value">{delay_frequency:.1f}%</div>
        <div class="kpi-subtitle">Shipments above threshold</div>
    </div>

    <div class="kpi-card">
        <div class="kpi-title">Route Efficiency Score</div>
        <div class="kpi-value">{route_efficiency_score:.1f}</div>
        <div class="kpi-subtitle">Normalized route performance</div>
    </div>

</div>
""")
st.divider()

# ==============================
# ROUTE EFFICIENCY OVERVIEW
# ==============================

st.markdown("<div class='section-title'><span>📊 Route Efficiency Overview</span></div>", unsafe_allow_html=True)

# Average Lead Time by Route
route_efficiency = (
    filtered_df.groupby("Region Route")
    .agg(
        Average_Lead_Time=("Lead Time", "mean"),
        Route_Volume=("Order ID", "nunique")
    )
    .reset_index()
)

# Route Efficiency Score
min_route_lead = route_efficiency["Average_Lead_Time"].min()
max_route_lead = route_efficiency["Average_Lead_Time"].max()

if max_route_lead > min_route_lead:
    route_efficiency["Route_Efficiency_Score"] = (
        100 * (
            1 -
            (
                route_efficiency["Average_Lead_Time"] - min_route_lead
            ) /
            (max_route_lead - min_route_lead)
        )
    )
else:
    route_efficiency["Route_Efficiency_Score"] = 100

# Round values
route_efficiency["Average_Lead_Time"] = (
    route_efficiency["Average_Lead_Time"].round(2)
)

route_efficiency["Route_Efficiency_Score"] = (
    route_efficiency["Route_Efficiency_Score"].round(2)
)

# --------------------------------
# Average Lead Time by Route
# --------------------------------

st.markdown("<div class='section-title'><span>🚚 Average Lead Time by Route</span></div>", unsafe_allow_html=True)

fig_route = px.bar(
    route_efficiency,
    x="Region Route",
    y="Average_Lead_Time",
    title="Average Lead Time by Route",
    labels={
        "Region Route": "Region Route",
        "Average_Lead_Time": "Average Lead Time (Days)"
    },
    custom_data=["Region Route"]
)
fig_route.update_layout(height=270, margin=dict(l=10,r=10,t=45,b=10), plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#243B53"), hoverlabel=dict(bgcolor="white"), showlegend=False)
fig_route.update_traces(marker_color="#1F6FEB", marker_line_width=0, hovertemplate="Route: %{x}<br>Avg Lead Time: %{y:.1f} days<extra></extra>")
route_event = st.plotly_chart(
    fig_route,
    use_container_width=True,
    key="route_chart_select",
    on_select="rerun",
    selection_mode="points"
)
route_point = _get_selection(route_event)
if route_point:
    route_value = _point_value(route_point, "customdata")
    if isinstance(route_value, (list, tuple)):
        route_value = route_value[0] if route_value else None
    if route_value:
        st.session_state.clicked_route = route_value
        st.session_state.clicked_region = str(route_value).replace("Factory → ", "")
        st.rerun()

# --------------------------------
# Top 10 Efficient Routes
# --------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section-title'><span>🏆 Top 10 Most Efficient Routes</span></div>", unsafe_allow_html=True)

    top_routes = (
        route_efficiency
        .sort_values("Route_Efficiency_Score", ascending=False)
        .head(10)
    )

    top_event = st.dataframe(
        top_routes,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="top_routes_table"
    )
    top_row = _get_selection(top_event)
    if top_row is not None and 0 <= top_row < len(top_routes):
        route_value = top_routes.iloc[top_row]["Region Route"]
        st.session_state.clicked_route = route_value
        st.session_state.clicked_region = str(route_value).replace("Factory → ", "")
        st.rerun()


# --------------------------------
# Bottom 10 Least Efficient Routes
# --------------------------------

with col2:
    st.markdown("<div class='section-title'><span>⚠️ Bottom 10 Least Efficient Routes</span></div>", unsafe_allow_html=True)

    bottom_routes = (
        route_efficiency
        .sort_values("Route_Efficiency_Score", ascending=True)
        .head(10)
    )

    bottom_event = st.dataframe(
        bottom_routes,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="bottom_routes_table"
    )
    bottom_row = _get_selection(bottom_event)
    if bottom_row is not None and 0 <= bottom_row < len(bottom_routes):
        route_value = bottom_routes.iloc[bottom_row]["Region Route"]
        st.session_state.clicked_route = route_value
        st.session_state.clicked_region = str(route_value).replace("Factory → ", "")
        st.rerun()

# ============================================================
# GEOGRAPHIC SHIPPING MAP
# ============================================================
st.markdown("<div class='section-title'><span>🗺️ Geographic Shipping Map</span></div>", unsafe_allow_html=True)

# Average lead time by state
state_efficiency = (
    df.groupby("State/Province")
    .agg(
        Average_Lead_Time=("Lead Time", "mean"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

# US State abbreviations
state_map = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ",
    "Arkansas": "AR", "California": "CA", "Colorado": "CO",
    "Connecticut": "CT", "Delaware": "DE", "Florida": "FL",
    "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}

state_efficiency["State_Code"] = (
    state_efficiency["State/Province"]
    .map(state_map)
)

# US Heatmap
fig = px.choropleth(
    state_efficiency.dropna(subset=["State_Code"]),
    locations="State_Code",
    locationmode="USA-states",
    color="Average_Lead_Time",
    scope="usa",
    hover_name="State/Province",
    custom_data=["State/Province"],
    hover_data={
        "Average_Lead_Time": ":.2f",
        "Total_Sales": ":.2f",
        "Gross_Profit": ":.2f"
    },
    title="US Shipping Efficiency by State"
)

fig.update_layout(height=430, margin=dict(l=5,r=5,t=45,b=5), paper_bgcolor="white", geo=dict(bgcolor="white"))

map_event = st.plotly_chart(
    fig,
    use_container_width=True,
    key="state_map_select",
    on_select="rerun",
    selection_mode="points"
)
map_point = _get_selection(map_event)
if map_point:
    state_value = _point_value(map_point, "customdata")
    if isinstance(state_value, (list, tuple)):
        state_value = state_value[0] if state_value else None
    if state_value:
        st.session_state.clicked_state = state_value
        st.rerun()

# ==============================
# REGIONAL SHIPPING BOTTLENECKS
# ==============================

regional_bottleneck = (
    df.groupby("Region Route")
      .agg(
          Average_Lead_Time=("Lead Time", "mean"),
          Shipment_Volume=("Order ID", "nunique")
      )
      .reset_index()
      .sort_values("Average_Lead_Time", ascending=False)
)

# Bottleneck identification
regional_bottleneck["Bottleneck"] = (
    regional_bottleneck["Average_Lead_Time"]
    > regional_bottleneck["Average_Lead_Time"].mean()
)

# Bar chart
fig_bottleneck = px.bar(
    regional_bottleneck,
    x="Region Route",
    y="Average_Lead_Time",
    color="Bottleneck",
    title="Regional Shipping Bottlenecks",
    labels={
        "Region Route": "Region Route",
        "Average_Lead_Time": "Average Lead Time (Days)"
    }
)
fig_bottleneck.update_layout(height=320, margin=dict(l=10,r=10,t=45,b=10), plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#243B53"))

fig_bottleneck.update_traces(
    customdata=regional_bottleneck[["Region Route"]].values
)
bottleneck_event = st.plotly_chart(
    fig_bottleneck,
    use_container_width=True,
    key="bottleneck_chart_select",
    on_select="rerun",
    selection_mode="points"
)
bottleneck_point = _get_selection(bottleneck_event)
if bottleneck_point:
    route_value = _point_value(bottleneck_point, "customdata")
    if isinstance(route_value, (list, tuple)):
        route_value = route_value[0] if route_value else None
    if route_value:
        st.session_state.clicked_route = route_value
        st.session_state.clicked_region = str(route_value).replace("Factory → ", "")
        st.rerun()

# Detailed table
bottleneck_table_event = st.dataframe(
    regional_bottleneck,
    use_container_width=True,
    hide_index=True,
    height=180,
    on_select="rerun",
    selection_mode="single-row",
    key="bottleneck_table"
)
bottleneck_table_row = _get_selection(bottleneck_table_event)
if bottleneck_table_row is not None and 0 <= bottleneck_table_row < len(regional_bottleneck):
    route_value = regional_bottleneck.iloc[bottleneck_table_row]["Region Route"]
    st.session_state.clicked_route = route_value
    st.session_state.clicked_region = str(route_value).replace("Factory → ", "")
    st.rerun()

# =====================================================
# SHIP MODE COMPARISON
# =====================================================

st.markdown("<div class='section-title'><span>🚛 Ship Mode Comparison</span></div>", unsafe_allow_html=True)

# Average Lead Time by Ship Mode
ship_mode_comparison = (
    df.groupby("Ship Mode")
    .agg(
       Average_Lead_Time=("Lead Time", "mean"),
        Total_Orders=("Ship Mode", "count")
    )
    .reset_index()
    .sort_values("Average_Lead_Time")
)

st.write("Average Lead Time by Shipping Method")

fig_ship_mode = px.bar(
    ship_mode_comparison,
    x="Ship Mode",
    y="Average_Lead_Time",
    title="Average Lead Time by Shipping Method",
    labels={
        "Ship Mode": "Ship Mode",
        "Average_Lead_Time": "Average Lead Time (Days)"
    },
    custom_data=["Ship Mode"]
)
fig_ship_mode.update_layout(height=270, margin=dict(l=10,r=10,t=45,b=10), plot_bgcolor="white", paper_bgcolor="white", font=dict(color="#243B53"), showlegend=False)
fig_ship_mode.update_traces(marker_color="#2F80ED", marker_line_width=0, hovertemplate="Ship Mode: %{x}<br>Avg Lead Time: %{y:.1f} days<extra></extra>")
ship_mode_event = st.plotly_chart(
    fig_ship_mode,
    use_container_width=True,
    key="ship_mode_chart_select",
    on_select="rerun",
    selection_mode="points"
)
ship_mode_point = _get_selection(ship_mode_event)
if ship_mode_point:
    ship_value = _point_value(ship_mode_point, "customdata")
    if isinstance(ship_value, (list, tuple)):
        ship_value = ship_value[0] if ship_value else None
    if ship_value:
        st.session_state.clicked_ship_mode = ship_value
        st.rerun()

st.markdown(
    "<h3 style='font-weight:800;'>Ship Mode Performance</h3>",
    unsafe_allow_html=True
)

ship_table_event = st.dataframe(
    ship_mode_comparison,
    use_container_width=True,
    hide_index=True,
    height=180,
    on_select="rerun",
    selection_mode="single-row",
    key="ship_mode_table"
)
ship_table_row = _get_selection(ship_table_event)
if ship_table_row is not None and 0 <= ship_table_row < len(ship_mode_comparison):
    ship_value = ship_mode_comparison.iloc[ship_table_row]["Ship Mode"]
    st.session_state.clicked_ship_mode = ship_value
    st.rerun()

# ============================================================
# ROUTE DRILL-DOWN
# ============================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #eaf3ff, #ffffff);
        padding: 8px 14px;
        border-radius: 10px;
        border-left: 6px solid #1f77b4;
        margin-top: 8px;
        margin-bottom: 8px;
    ">
        <h2 style="
            margin: 0;
            color: #172b4d;
            font-size: 20px;
            font-weight: 800;
        ">
            Route Drill-Down
        </h2>
        <p style="
            margin: 5px 0 0 0;
            color: #4a5568;
            font-size: 12px;
        ">
            Detailed state-level and order-level shipping performance
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# STATE-LEVEL PERFORMANCE
# ============================================================

st.markdown(
    """
    <h3 style="
        color: #172b4d;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 10px;
    ">
        State-Level Performance Insights
    </h3>
    """,
    unsafe_allow_html=True
)

state_performance = (
    df.groupby(["Region Route", "State/Province"])
    .agg(
        Average_Lead_Time=("Lead Time", "mean"),
        Total_Orders=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values("Average_Lead_Time")
)


# Format numbers
state_performance["Average_Lead_Time"] = (
    state_performance["Average_Lead_Time"].round(2)
)

state_performance["Total_Sales"] = (
    state_performance["Total_Sales"].round(2)
)

state_performance["Gross_Profit"] = (
    state_performance["Gross_Profit"].round(2)
)

# Attractive table styling
state_styled = (
    state_performance.style
    .set_properties(**{
        "color": "#000000",
        "font-size": "14px"
    })
    .set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#1f4e78"),
                ("color", "white"),
                ("font-weight", "bold"),
                ("font-size", "14px"),
                ("text-align", "center")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("color", "#000000"),
                ("padding", "8px"),
                ("border-bottom", "1px solid #e2e8f0")
            ]
        },
        {
            "selector": "tbody tr:nth-child(even)",
            "props": [
                ("background-color", "#f4f8fb")
            ]
        },
        {
            "selector": "tbody tr:hover",
            "props": [
                ("background-color", "#e6f2ff")
            ]
        }
    ])
    .format({
        "Average_Lead_Time": "{:.2f}",
        "Total_Orders": "{:,.0f}",
        "Total_Sales": "{:,.2f}",
        "Gross_Profit": "{:,.2f}"
    })
)

state_table_event = st.dataframe(
    state_styled,
    width="stretch",
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    key="state_performance_table"
)
state_table_row = _get_selection(state_table_event)
if state_table_row is not None and 0 <= state_table_row < len(state_performance):
    state_value = state_performance.iloc[state_table_row]["State/Province"]
    st.session_state.clicked_state = state_value
    st.rerun()

# ============================================================
# ORDER-LEVEL SHIPMENT TIMELINE
# ============================================================

st.markdown(
    """
    <h3 style="
        color: #172b4d;
        font-weight: 800;
        margin-top: 25px;
        margin-bottom: 10px;
    ">
        Order-Level Shipment Timeline
    </h3>
    """,
    unsafe_allow_html=True
)

# Order selector
order_options = df["Order ID"].dropna().unique()
if st.session_state.clicked_order in order_options:
    default_order_index = list(order_options).index(st.session_state.clicked_order)
else:
    default_order_index = 0
selected_order = st.selectbox(
    "Select an Order ID",
    order_options,
    index=default_order_index,
    key="order_selector"
)
st.session_state.clicked_order = selected_order


# Selected order details
order_details = df[
    df["Order ID"] == selected_order
].drop_duplicates(subset=["Order ID"], keep="first")
[
    [
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "State/Province",
        "Region Route",
        "Lead Time",
        "Sales",
        "Gross Profit"
    ]
].copy()


# Round numeric values
order_details["Lead Time"] = order_details["Lead Time"].round(2)
order_details["Sales"] = order_details["Sales"].round(2)
order_details["Gross Profit"] = order_details["Gross Profit"].round(2)


# Attractive order table
order_styled = (
    order_details.style
    .set_properties(
        **{
            "color": "#172b4d",
            "font-weight": "600",
            "font-size": "14px"
        }
    )
    .set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("background-color", "#1f4e78"),
                    ("color", "white"),
                    ("font-weight", "bold"),
                    ("font-size", "14px"),
                    ("text-align", "center")
                ]
            },
            {
                "selector": "td",
                "props": [
                    ("padding", "8px"),
                    ("border-bottom", "1px solid #e2e8f0")
                ]
            }
        ]
    )
)

order_table_event = st.dataframe(
    order_styled,
    width="stretch",
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    key="order_details_table"
)
order_table_row = _get_selection(order_table_event)
if order_table_row is not None and 0 <= order_table_row < len(order_details):
    st.session_state.clicked_order = order_details.iloc[order_table_row]["Order ID"]
    st.rerun()


# Shipment Timeline Data
timeline_data = order_details[
    ["Order ID", "Order Date", "Ship Date"]
].copy()

timeline_data["Order Date"] = pd.to_datetime(
    timeline_data["Order Date"]
)

timeline_data["Ship Date"] = pd.to_datetime(
    timeline_data["Ship Date"]
)

timeline_data["Shipment Days"] = (
    timeline_data["Ship Date"] -
    timeline_data["Order Date"]
).dt.days

st.write("Shipment Timeline")

st.dataframe(
    timeline_data,
    width="stretch",
    hide_index=True
)



st.markdown("<div style='text-align:center;color:#829AB1;font-size:11px;padding:14px 0 4px 0;'>Nassau Candy Shipping Analytics • Interactive Streamlit Dashboard</div>", unsafe_allow_html=True)
