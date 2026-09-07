import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 30)

# Load dataset
file_path = "Data/Nassau Candy Distributor (2).csv"
df = pd.read_csv(file_path)

# Basic dataset check
print("Rows and Columns:", df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())
print("\nDuplicate Rows:", df.duplicated().sum())

print("\nDate Range:")
print("Order Date:", df["Order Date"].min(), "to", df["Order Date"].max())
print("Ship Date:", df["Ship Date"].min(), "to", df["Ship Date"].max())
# Date validation
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")

print("\nInvalid Order Dates:", df["Order Date"].isna().sum())
print("Invalid Ship Dates:", df["Ship Date"].isna().sum())

# Calculate shipping lead time
lead_time = (df["Ship Date"] - df["Order Date"]).dt.days

print("\nShipping Lead Time Summary:")
print(lead_time.describe())

print("\nNegative Lead Time:", (lead_time < 0).sum())
print("\nSample Date Records:")
print(df[["Order ID", "Order Date", "Ship Date"]].head(10).to_string(index=False))
print("\nConverted Date Range:")
print("Order Date:", df["Order Date"].min().date(), "to", df["Order Date"].max().date())
print("Ship Date:", df["Ship Date"].min().date(), "to", df["Ship Date"].max().date())

# Create Shipping Lead Time
df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

print("\nLead Time Check:")
print(df[["Order ID", "Order Date", "Ship Date", "Lead Time"]].head(10).to_string(index=False))

print("\nLead Time Summary:")
print(df["Lead Time"].describe())

print("\nData Types:")
print(df.dtypes)

# Check numeric columns
numeric_columns = ["Sales", "Units", "Gross Profit", "Cost", "Lead Time"]

print("\nNumeric Data Summary:")
print(df[numeric_columns].describe())

print("\nNegative Values:")
for col in numeric_columns:
    print(col, ":", (df[col] < 0).sum())

    # Check zero values
print("\nZero Values:")

for col in numeric_columns:
    print(col, ":", (df[col] == 0).sum())

    # Check categorical columns
categorical_columns = ["Ship Mode", "Country/Region", "Division", "Region"]

print("\nUnique Values in Categorical Columns:")

for col in categorical_columns:
    print(f"\n{col}:")
    print(df[col].unique())

    # Check leading/trailing spaces in text columns
text_columns = df.select_dtypes(include="object").columns

print("\nText Columns with Extra Spaces:")

for col in text_columns:
    spaces = (df[col].astype(str) != df[col].astype(str).str.strip()).sum()
    if spaces > 0:
        print(col, ":", spaces)

        # =========================
# FINAL DATA CLEANING
# =========================

# Remove duplicate rows if any
df = df.drop_duplicates()

# Remove extra spaces from text columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# Ensure date columns are in datetime format
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

# Create shipping lead time
df["Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

print("\nFinal Cleaned Dataset:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Missing Values:", df.isnull().sum().sum())
print("Duplicate Rows:", df.duplicated().sum())

# =========================
# SALES ANALYSIS
# =========================

print("\nSales Analysis:")

print("Total Sales:", df["Sales"].sum())
print("Average Sales:", df["Sales"].mean())
print("Minimum Sales:", df["Sales"].min())
print("Maximum Sales:", df["Sales"].max())

print("\nSales by Region:")
print(df.groupby("Region")["Sales"].sum().sort_values(ascending=False))

# =========================
# PROFIT ANALYSIS
# =========================

print("\nProfit Analysis:")

print("Total Gross Profit:", df["Gross Profit"].sum())
print("Average Gross Profit:", df["Gross Profit"].mean())
print("Minimum Gross Profit:", df["Gross Profit"].min())
print("Maximum Gross Profit:", df["Gross Profit"].max())

print("\nGross Profit by Region:")
print(df.groupby("Region")["Gross Profit"].sum().sort_values(ascending=False))

# =========================
# SHIP MODE ANALYSIS
# =========================

print("\nSales by Ship Mode:")
print(df.groupby("Ship Mode")["Sales"].sum().sort_values(ascending=False))

print("\nGross Profit by Ship Mode:")
print(df.groupby("Ship Mode")["Gross Profit"].sum().sort_values(ascending=False))

# =========================
# PRODUCT ANALYSIS
# =========================

print("\nTop 10 Products by Sales:")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)

print("\nTop 10 Products by Gross Profit:")

top_profit_products = (
    df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_profit_products)

# =========================
# REGIONAL ANALYSIS
# =========================

print("\nSales and Profit by Region:")

region_analysis = (
    df.groupby("Region")[["Sales", "Gross Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
)

print(region_analysis)

# =========================
# STATE-WISE ANALYSIS
# =========================

print("\nTop 10 States by Sales:")

state_sales = (
    df.groupby("State/Province")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(state_sales)

# =========================
# STATE-WISE GROSS PROFIT
# =========================

print("\nTop 10 States by Gross Profit:")

state_profit = (
    df.groupby("State/Province")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(state_profit)

# =========================
# SALES AND PROFIT BY SHIP MODE
# =========================

print("\nSales and Gross Profit by Ship Mode:")

ship_mode_analysis = (
    df.groupby("Ship Mode")[["Sales", "Gross Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
)

print(ship_mode_analysis)

# =========================
# REGION-WISE LEAD TIME ANALYSIS
# =========================

print("\nAverage Lead Time by Region:")

region_lead_time = (
    df.groupby("Region")["Lead Time"]
    .mean()
    .sort_values(ascending=False)
)

print(region_lead_time)

# =========================
# TOP 10 PRODUCTS BY UNITS SOLD
# =========================

print("\nTop 10 Products by Units Sold:")

top_products_units = (
    df.groupby("Product Name")["Units"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products_units)

# =========================
# SALES TREND BY MONTH
# =========================

print("\nMonthly Sales Trend:")

monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

print(monthly_sales)

# =========================
# MONTHLY GROSS PROFIT TREND
# =========================

print("\nMonthly Gross Profit Trend:")

monthly_profit = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Gross Profit"]
    .sum()
)

print(monthly_profit)

# =========================
# LEAD TIME BY SHIP MODE
# =========================

print("\nAverage Lead Time by Ship Mode:")

lead_time_ship_mode = (
    df.groupby("Ship Mode")["Lead Time"]
    .mean()
    .sort_values(ascending=False)
)

print(lead_time_ship_mode)

# =========================
# SALES & GROSS PROFIT BY STATE
# =========================

print("\nSales & Gross Profit by State:")

state_analysis = (
    df.groupby("State/Province")[["Sales", "Gross Profit"]]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

print(state_analysis)

# =========================
# LEAD TIME ANALYSIS
# =========================

print("\nLead Time Analysis:")

print("\nOverall Lead Time:")
print(df["Lead Time"].describe())

print("\nAverage Lead Time by Region:")
print(
    df.groupby("Region")["Lead Time"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Lead Time by Ship Mode:")
print(
    df.groupby("Ship Mode")["Lead Time"]
    .mean()
    .sort_values(ascending=False)
)

# =========================
# FINAL KEY INSIGHTS
# =========================

print("\n=========================")
print("FINAL KEY INSIGHTS")
print("=========================")

# Best performing region by sales
best_region = df.groupby("Region")["Sales"].sum().idxmax()
best_region_sales = df.groupby("Region")["Sales"].sum().max()

print("\nBest Region by Sales:")
print(best_region, "->", round(best_region_sales, 2))

# Best performing region by profit
best_profit_region = df.groupby("Region")["Gross Profit"].sum().idxmax()
best_region_profit = df.groupby("Region")["Gross Profit"].sum().max()

print("\nBest Region by Gross Profit:")
print(best_profit_region, "->", round(best_region_profit, 2))

# Best ship mode by sales
best_ship_mode = df.groupby("Ship Mode")["Sales"].sum().idxmax()
best_ship_mode_sales = df.groupby("Ship Mode")["Sales"].sum().max()

print("\nBest Ship Mode by Sales:")
print(best_ship_mode, "->", round(best_ship_mode_sales, 2))

# Fastest ship mode
fastest_ship_mode = df.groupby("Ship Mode")["Lead Time"].mean().idxmin()
fastest_lead_time = df.groupby("Ship Mode")["Lead Time"].mean().min()

print("\nFastest Ship Mode by Average Lead Time:")
print(fastest_ship_mode, "->", round(fastest_lead_time, 2), "days")

# Top product by sales
top_product = df.groupby("Product Name")["Sales"].sum().idxmax()
top_product_sales = df.groupby("Product Name")["Sales"].sum().max()

print("\nTop Product by Sales:")
print(top_product, "->", round(top_product_sales, 2))


# =========================
# ROUTE CREATION
# =========================

# Create Factory to Customer Region route
df["Region Route"] = "Factory → " + df["Region"].astype(str)

# Create Factory to Customer State route
df["State Route"] = "Factory → " + df["State/Province"].astype(str)

print("\nRoute Columns Created:")

print("\nSample Region Routes:")
print(df["Region Route"].head(10))

print("\nSample State Routes:")
print(df["State Route"].head(10))

# =========================
# AVERAGE LEAD TIME BY ROUTE
# =========================

avg_lead_time_by_region = (
    df.groupby("Region Route")["Lead Time"]
    .mean()
    .sort_values()
)

print("\nAverage Lead Time by Region Route:")
print(avg_lead_time_by_region.round(2))

# =========================
# ROUTE PERFORMANCE LEADERBOARD
# =========================

print("\nRoute Performance - Fastest Routes:")
print(avg_lead_time_by_region.head(4).round(2))

print("\nRoute Performance - Slowest Routes:")
print(avg_lead_time_by_region.sort_values(ascending=False).head(4).round(2))


# =========================
# STATE-LEVEL SHIPPING PERFORMANCE
# =========================

state_shipping = df.groupby("State/Province").agg(
    Average_Lead_Time=("Lead Time", "mean"),
    Total_Sales=("Sales", "sum"),
    Gross_Profit=("Gross Profit", "sum")
).sort_values("Average_Lead_Time", ascending=False)

print("\nState-Level Shipping Performance:")
print(state_shipping.round(2))

# =========================
# ORDER-LEVEL SHIPMENT TIMELINE
# =========================

# Convert dates to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Calculate shipment duration
df["Shipment Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

print("\nOrder-Level Shipment Timeline:")

order_timeline = df[
    [
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Region",
        "State/Province",
        "Shipment Days"
    ]
].copy()

print(order_timeline.head(20))


# =========================
# GEOGRAPHIC SHIPPING MAP
# =========================

# US State abbreviations
state_codes = {
    "Alabama": "AL", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
    "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
    "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}

# Create state code
df["State Code"] = df["State/Province"].map(state_codes)

# Keep only US states for map
us_map_data = df[df["State Code"].notna()].groupby(
    ["State/Province", "State Code"]
).agg(
    Average_Lead_Time=("Lead Time", "mean"),
    Total_Sales=("Sales", "sum"),
    Gross_Profit=("Gross Profit", "sum")
).reset_index()

print("\nGeographic Shipping Map Data:")
print(us_map_data.head(20))


# =========================
# REGIONAL BOTTLENECK ANALYSIS
# =========================

regional_bottlenecks = df.groupby("Region").agg(
    Average_Lead_Time=("Lead Time", "mean"),
    Total_Sales=("Sales", "sum"),
    Gross_Profit=("Gross Profit", "sum")
).sort_values(
    "Average_Lead_Time",
    ascending=False
)

print("\nRegional Bottleneck Analysis:")
print(regional_bottlenecks.round(2))


# =========================
# DASHBOARD DATA PREPARATION
# =========================

print("\n" + "=" * 60)
print("DASHBOARD DATA PREPARATION")
print("=" * 60)

# KPI Summary
total_sales = df["Sales"].sum()
total_profit = df["Gross Profit"].sum()
avg_lead_time = df["Lead Time"].mean()
total_orders = df["Order ID"].nunique()

print("\nKPI SUMMARY:")
print("Total Orders:", total_orders)
print("Total Sales:", round(total_sales, 2))
print("Total Gross Profit:", round(total_profit, 2))
print("Average Lead Time:", round(avg_lead_time, 2))



















