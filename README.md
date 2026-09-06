# 🛡️ Universal Cyber Shield AI — SVM Phishing/Fraud Website Scanner

A Streamlit-based web app that uses a **Support Vector Machine (SVM)** model to detect phishing / fraudulent websites based on structural URL features (domain age, SSL status, redirects, scam keywords, etc.). Supports **English & Hindi** interface and generates a **PDF forensics report**.

## ✨ Features

- 🔍 Live URL risk scanner with 13 input features
- 🌐 Dual language support (English / Hindi)
- 📋 Detailed forensics report generation
- 📥 Downloadable PDF report
- 🎨 Custom dark/cyberpunk UI theme

## 📁 Project Structure

```
├── cyber_shield_app.py           # Main Streamlit application
├── requirements.txt              # Python dependencies
├── svm_cyber_shield_model.pkl    # Trained SVM model (not included — see below)
├── svm_cyber_shield_scaler.pkl   # StandardScaler used during training
├── svm_model_features.pkl        # Feature order used during training
└── README.md
```

## ⚠️ Model Files

This repo requires three `.pkl` files (`svm_cyber_shield_model.pkl`, `svm_cyber_shield_scaler.pkl`, `svm_model_features.pkl`) trained separately.

- **If small (< 25 MB total):** they can be committed directly to the repo.
- **If large:** use [Git LFS](https://git-lfs.com/) or host them externally (e.g. Google Drive, Hugging Face Hub) and download them in a setup step.

If these files are missing, the app will show a clear error message on startup instead of crashing.

## 🚀 Setup & Run Locally

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd <your-repo-folder>

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Make sure the 3 .pkl model files are in the project root

# 5. Run the app
streamlit run cyber_shield_app.py
```

## 🖥️ Usage

1. Open the app in your browser (Streamlit will give you a local URL, usually `http://localhost:8501`)
2. Select your preferred language (English/Hindi) from the sidebar
3. Enter the suspect URL and adjust the feature sliders/inputs
4. Click **"Initiate High-Secure Scan"**
5. View the result and download the PDF forensics report from the second tab

## 🛡️ Disclaimer

This tool is for educational/demonstration purposes. It uses a geometric SVM model to estimate risk — always verify suspicious links independently and never enter sensitive information on unverified websites. Report phishing to India's Cyber Crime Helpline: **1930** or [cybercrime.gov.in](https://cybercrime.gov.in).

## 📄 License

Add your license here (e.g. MIT).
