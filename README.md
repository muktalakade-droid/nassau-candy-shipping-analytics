# Nassau Candy – Shipping Route Efficiency Analytics

## Project Overview

This project analyzes shipping route efficiency for Nassau Candy Distributor using an interactive Streamlit dashboard.

The dashboard provides insights into route performance, shipping lead time, geographic bottlenecks, shipping methods, state-level performance, and order-level shipment timelines.

## Key Features

- Route Efficiency Overview
- Average Lead Time by Route
- Top 10 Most Efficient Routes
- Bottom 10 Least Efficient Routes
- Geographic Shipping Map
- Regional Bottleneck Analysis
- Ship Mode Comparison
- Ship Mode Performance
- Route Drill-Down
- State-Level Performance Insights
- Order-Level Shipment Timeline
- Date Range Filter
- Region Filter
- State Filter
- Ship Mode Filter
- Lead-Time Threshold Filter
- Order ID Selection

## Technologies Used

- Python
- Pandas
- NumPy
- Streamlit
- Plotly

## Project Structure

- `app.py` – Streamlit dashboard application
- `main.py` – Main Python project file
- `requirements.txt` – Required Python libraries
- `Data/` – Dataset used for the analysis

## Dataset

The project uses the Nassau Candy Distributor dataset to analyze shipping routes, shipment lead time, shipping modes, states, orders, sales, and profit.

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt

Run the Streamlit dashboard:

streamlit run app.py
Dashboard

The interactive dashboard helps analyze:

Shipping lead time
Route efficiency
Geographic shipping performance
Regional bottlenecks
Shipping mode performance
State-level performance
Order-level shipment timelines
Project Purpose

The purpose of this project is to analyze shipping efficiency and identify routes, regions, states, and shipping methods that may require improvement.