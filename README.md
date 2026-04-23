# Cricbuzz Live Stats Dashboard

A professional Streamlit-based data analytics dashboard that provides real-time and recent cricket match insights using RapidAPI.

---

## Features

- Live & recent match tracking
- Match statistics and analytics
- Team and venue insights
- Interactive visualisations (Plotly)
- Clean and modern UI using Streamlit
- Secure API key handling with environment variables

---

## Dashboard Modules

- Home → Overview with KPIs (Total Matches, Live Matches, Teams, Venues)
- Live → Real-time match data
- Players → Player-related insights
- Analytics → Charts & distributions
- SQL → Query-based insights
- CRUD → Data operations

---

## Tech Stack

- Python 3
- Streamlit
- Pandas
- Plotly
- Requests
- RapidAPI (Cricket Live Line API)

---

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Cricbuzz_LiveStats.git
cd Cricbuzz_LiveStats 
```
### 2. Create a virtual environment
``` bash
python -m venv .venv
source .venv/bin/activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add API Key
   Create .env file:
```
RAPIDAPI_KEY=your_api_key_here
```

▶️ Run the app
```
streamlit run app.py
```
☁️ Deployment (Streamlit Cloud)
  Push code to GitHub
  Go to Streamlit Cloud
  Add secret:
```
RAPIDAPI_KEY="your_api_key_here"
```

## 🎥 Demo Video

[![Watch the video](https://youtu.be/9SQNvkZtwzg)

## 🌐 Live App

👉 (https://cricbuzzlivestats-lzplbdlhufhk8mfpa7pnkc.streamlit.app/)

👨‍💻 Author

Achintya Krishna
