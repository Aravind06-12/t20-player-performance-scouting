# T20 Player Performance Scouting

A data analytics project that processes IPL ball-by-ball data
and builds player performance metrics for T20 scouting.

## Data Source

Cricket match data is sourced from Cricsheet.

The raw JSON files are kept locally and are not committed
to GitHub.

## Current Dataset

- IPL matches processed: 1,243
- Delivery records processed: 295,732
- Failed matches: 0

## Project Pipeline

Cricsheet JSON
→ ingestion
→ processed match/delivery tables
→ batting & bowling analytics
→ phase analytics
→ player performance scoring
→ scouting metrics

## Project Structure

t20-player-performance-scouting/
├── data/
│   ├── raw/
│   ├── processed/
│   └── analytics/
├── notebooks/
├── src/
│   ├── config.py
│   ├── ingestion.py
│   ├── analytics.py
│   └── pipeline.py
├── tests/
├── outputs/
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE

## Running the Pipeline

Activate the virtual environment and run:

python -m src.pipeline

## Testing

Run:

python -m pytest tests -v

## Status

Core Project 1 pipeline completed and validated.
