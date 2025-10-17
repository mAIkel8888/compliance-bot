 ========================================
# ALLE DATEIEN FÜR STREAMLIT CLOUD SETUP
# ========================================

# ----------------
# 1. app.py
# ----------------
cat > app.py << 'EOF'
import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="🌿 Compliance Bot",
    page_icon="🌿",
    layout="wide"
)

# CSS Styling
st.markdown("""
<style>
    .main {padding: 2rem;}
    .stAlert {border-radius: 0.5rem;}
    div[data-testid="stMetricValue"] {font-size: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("🌿 Compliance Bot")
st.markdown("**KI-gestützte Analyse von Umwelt-Claims**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Einstellungen")
    webhook_url = st.text_input(
        "n8n Webhook URL",
        value=st.secrets.get("N8N_WEBHOOK_URL", ""),
        type="password",
        help="Deine n8n Webhook URL"
    )
    
    st.divider()
    st.info("""
    ### 📖 Anleitung
    1. Dokument hochladen
    2. Analysieren klicken
    3. Ergebnisse prüfen
    
    ### 🎯 Formate
    PDF, DOCX, TXT
    """)

# Main Area
uploaded_file = st.file_uploader(
    "📄 Dokument hochladen",
    type=['pdf', 'docx', 'txt']
)

if uploaded_file:
    st.success(f"✅ {uploaded_file.name} ({uploaded_file.size/1024:.1f} KB)")

analyze = st.button("🔍 Analysieren", type="primary", disabled=not uploaded_file)

if analyze and uploaded_file:
    with st.spinner("🤖 Analysiere..."):
        try:
            files = {'data': (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(webhook_url, files=files, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Analyse abgeschlossen!")
                
                if result.get('summary'):
                    summary = result['summary']
                    
                    # Metriken
                    cols = st.columns(4)
                    cols[0].metric("Gesamt", summary.get('total_claims', 0))
                    cols[1].metric("Kritisch", summary.get('critical_count', 0), delta=f"-{summary.get('critical_count', 0)}", delta_color="inverse")
                    cols[2].metric("Bedenklich", summary.get('concerning_count', 0))
                    cols[3].metric("Unkritisch", summary.get('safe_count', 0), delta=f"+{summary.get('safe_count', 0)}")
                    
                    st.divider()
                    
                    # Risiko
                    risk = summary.get('overall_risk', 'UNBEKANNT')
                    if risk == 'HOCH':
                        st.error(f"⚠️ Gesamt-Risiko: {risk}")
                    elif risk == 'MITTEL':
                        st.warning(f"⚡ Gesamt-Risiko: {risk}")
                    else:
                        st.success(f"✅ Gesamt-Risiko: {risk}")
                    
                    # Kritische Claims
                    if result.get('critical_claims'):
                        st.header("🚨 Kritische Claims")
                        for idx, claim in enumerate(result['critical_claims'], 1):
                            with st.expander(f"Claim {idx}: {claim['text'][:50]}..."):
                                st.markdown(f"**Risiko:** {claim.get('risk_level')}")
                                st.subheader("Probleme:")
                                for issue in claim.get('issues', []):
                                    st.markdown(f"- {issue}")
                                if claim.get('recommendations'):
                                    st.subheader("Empfehlungen:")
                                    for rec in claim['recommendations']:
                                        st.markdown(f"- {rec}")
                    
                    # Download
                    st.divider()
                    st.download_button(
                        "📥 Report herunterladen",
                        json.dumps(result, indent=2, ensure_ascii=False),
                        file_name=f"report_{datetime.now():%Y%m%d_%H%M%S}.json",
                        mime="application/json"
                    )
                else:
                    st.info("ℹ️ Keine Claims gefunden")
            else:
                st.error(f"Fehler: HTTP {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")

st.divider()
st.markdown("<center>Powered by n8n + GPT-4 + Streamlit</center>", unsafe_allow_html=True)
EOF


# ----------------
# 2. requirements.txt
# ----------------
cat > requirements.txt << 'EOF'
streamlit==1.31.0
requests==2.31.0
EOF


# ----------------
# 3. .streamlit/config.toml
# ----------------
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false
EOF


# ----------------
# 4. .gitignore
# ----------------
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.env
.DS_Store
venv/
*.egg-info/
.streamlit/secrets.toml
EOF


# ----------------
# 5. README.md
# ----------------
cat > README.md << 'EOF'
# 🌿 Compliance Bot

KI-gestützte Analyse von Umwelt-Claims in Marketing-Materialien.

## Deployment

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## Setup

1. Fork this repository
2. Deploy on Streamlit Cloud
3. Add Secret: `N8N_WEBHOOK_URL`

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features

- 📄 PDF, DOCX, TXT Upload
- 🤖 GPT-4 Analyse
- 📊 Visualisierung
- 📥 JSON Export
EOF


# ----------------
# Dateien committen
# ----------------
git add .
git commit -m "Initial Streamlit Cloud setup"
git push


echo "=========================================="
echo "✅ SETUP ABGESCHLOSSEN!"
echo "=========================================="
echo ""
echo "Nächste Schritte:"
echo "1. Gehe zu: https://share.streamlit.io"
echo "2. Klicke 'New app'"
echo "3. Wähle dein Repository"
echo "4. Main file: app.py"
echo "5. Add Secret: N8N_WEBHOOK_URL"
echo "6. Deploy!"
echo ""
