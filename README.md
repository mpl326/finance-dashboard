📊 Earnings Call Sentiment & Event Study Dashboard

This project analyzes earnings call sentiment (management remarks + Q&A) and links it to stock performance using an event study methodology.
The final output is an interactive Streamlit dashboard that allows users to explore how sentiment relates to abnormal returns (CAR) across multiple event windows.

📁 Repository Structure
finance-dashboard/
│
├── Dashboard_app.py                     # Streamlit dashboard application
├── Data_Analysis_and_EDSL_results.ipynb # Notebook that generates dataset
├── data/                                 # (create this folder locally)
│   └── README.md                         # instructions for placing CSV
└── README.md                             # project documentation


⚙️ Generating the Dataset (Important)

The dataset is not included in this repository because the file size exceeds GitHub’s limits.

To generate the required CSV:

Open Data_Analysis_and_EDSL_results.ipynb in Google Colab.

Run all cells until the file dashboard_event_study_data.csv is created.

Download that CSV to your computer.

Create a local folder named data/ in your repo.

Move the CSV into the data/ folder.

▶️ Running the Streamlit Dashboard
Once the dataset is in the data/ folder, run:
pip install streamlit pandas altair
streamlit run Dashboard_app.py

🧠 Features of the Dashboard

Select company ticker

Filter by earnings event date range

Compare CAR windows:

Anticipation window

Tight event window

Post-event drift

Total window

Sentiment vs CAR scatter plot

Per-event and average CAR window visualizations

Full event table with sentiment + CAR metrics

Interactive Altair visualizations

🔧 Technologies Used

Python

Pandas

Streamlit

Altair

Google Colab







