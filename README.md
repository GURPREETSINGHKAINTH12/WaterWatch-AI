# WaterWatch AI
**AI-powered water-quality anomaly detection and risk-screening prototype**  
SDG 6: Clean Water and Sanitation

## Features
- CSV upload and manual sample entry
- Rule-based screening against configurable reference thresholds
- Isolation Forest anomaly detection
- Random Forest demonstration classification trained on bundled *synthetic demonstration data*
- Historical sample storage using SQLite
- Interactive trend charts
- English/Hindi interface labels
- Explainable, cautious next-step guidance

## Important safety and scientific limitations
This is an educational prototype, not a certified drinking-water testing system. The bundled `data/demo_water_quality.csv` is synthetic and is used to demonstrate software functionality. Its `demo_reference_label` is not a laboratory result and must not be interpreted as ground truth. Model outputs are not validated for public-health decisions. Some contaminants (including pathogens and many chemicals) cannot be inferred from the included parameters. Use certified laboratory testing and applicable local standards for drinking-water decisions.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
The core demo works locally after dependencies are installed. Internet is only needed to install packages or access external data/services.

## Dataset
`data/demo_water_quality.csv` contains synthetic sample records for demonstration only. Replace it with a documented, appropriately licensed real dataset before making empirical claims. Recommended sources to investigate:
- WHO drinking-water guidelines: https://www.who.int/publications/i/item/9789240045064
- India National Water Data Portal / CPCB datasets: https://nwdp.nwic.gov.in/
- Water Potability dataset (verify source, license, and label definition before use): https://huggingface.co/datasets/Kavi-ya/Water-Potability

## Project structure
- `app.py`: Streamlit dashboard
- `src/`: preprocessing, models, screening, database, translations
- `data/`: synthetic demonstration CSV
- `tests/`: basic tests
