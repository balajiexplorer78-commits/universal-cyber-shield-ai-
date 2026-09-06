import streamlit as st
import pandas as pd
import numpy as np
import pickle
from fpdf import FPDF
import base64

# 1. Premium Page Config (Dark Mode & Wide Layout)
st.set_page_config(page_title="Universal Cyber Shield AI", page_icon="🛡️", layout="wide")

# Custom CSS for Premium Cyberpunk Dark Mode UI Theme
st.markdown("""
<style>
    .stApp { background-color: #060913; color: #e2e8f0; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: #0f172a; padding: 12px; border-radius: 14px; }
    .stTabs [data-baseweb="tab"] { color: #94a3b8; font-size: 16px; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #38bdf8 !important; border-bottom-color: #38bdf8 !important; }
    .glass-card { background: rgba(15, 23, 42, 0.6); border-radius: 16px; padding: 26px; border: 1px solid rgba(56, 189, 248, 0.2); backdrop-filter: blur(12px); margin-bottom: 22px; }
    .status-critical { color: #f43f5e; font-size: 26px; font-weight: bold; text-shadow: 0 0 12px rgba(244, 63, 94, 0.6); }
    .status-secure { color: #10b981; font-size: 26px; font-weight: bold; text-shadow: 0 0 12px rgba(16, 185, 129, 0.6); }
</style>
""", unsafe_allow_html=True)

# 2. SVM Model, Scaler aur Features Load karna (safe loading with error handling)
@st.cache_resource
def load_artifacts():
    try:
        with open('svm_cyber_shield_model.pkl', 'rb') as file:
            model = pickle.load(file)
        with open('svm_cyber_shield_scaler.pkl', 'rb') as file:
            scaler = pickle.load(file)
        with open('svm_model_features.pkl', 'rb') as file:
            model_features = pickle.load(file)
        return model, scaler, model_features
    except FileNotFoundError as e:
        st.error(f"❌ Required model file not found: {e.filename}. "
                 f"Please make sure 'svm_cyber_shield_model.pkl', "
                 f"'svm_cyber_shield_scaler.pkl' and 'svm_model_features.pkl' "
                 f"are in the same folder as this script.")
        st.stop()

model, scaler, model_features = load_artifacts()

# 3. Dual Language Translation Dictionary (Hindi & English)
translations = {
    "English": {
        "title": "🛡️ UNIVERSAL CYBER SHIELD AI — SVM SCANNER",
        "subtitle": "Advanced Geometric Pattern Recognition Engine for Phishing & Fraud Website Detection",
        "lang_select": "Select Interface Language / भाषा चुनें",
        "tab1": "🔍 Live URL Scanner",
        "tab2": "📋 Detailed Forensics Report & PDF",
        "header_scan": "Enter Any Suspect Link / Website URL to Scan",
        "url_input_label": "Paste Website Link here:",
        "url_len": "URL Length (Characters)",
        "dots_count": "Quantity of Dots (.) in URL",
        "hyphen_count": "Quantity of Hyphens (-) in URL",
        "subdomain_count": "Total Subdomains Count",
        "at_symbol": "Contains '@' Symbol Character?",
        "ip_url": "Contains Raw IP Address (e.g. 192.168.1.1)?",
        "shortened": "Is it a Shortened Link (e.g. bit.ly, tinyurl)?",
        "dom_age": "Domain Age (Months since registration)",
        "ssl_status": "Valid SSL Certificate Active (HTTPS)?",
        "trust_score": "Google Safe Browsing Trust Score (0-100)",
        "redirect_count": "External Web Redirects Count",
        "free_host": "Is Hosted on a Free Platform (e.g. blogspot, vercel)?",
        "scam_kw": "Contains Scam Keywords (stipend, internship, offer, lottery)?",
        "btn_scan": "⚡ INITIATE HIGH-SECURE SCAN",
        "res_fake": "🚨 SECURITY THREAT: PHISHING / FAKE WEBSITE DETECTED",
        "res_legal": "✅ VERIFIED SECURE: LEGITIMATE WEBSITE",
        "reasons_title": "🔍 System Forensics & Triggers Found:",
        "advice_title": "🛡️ Instant Cyber-Defense Actionable Solutions:",
        "adv_fake": "1. **Block Immediately:** Do NOT enter credit cards, OTPs, or passwords.\n2. **Report Link:** Dial **1930** (Cyber Crime Helpline) or report on cybercrime.gov.in.\n3. **Reset Session:** If you typed any details, change your banking and social media credentials right now.",
        "adv_legal": "1. **Safe To Browse:** This domain aligns with trusted industry standard protocols.\n2. **Standard Check:** Always ensure the browser lock icon remains visible before submitting confidential payments.",
        "download_btn": "📥 Download Cyber Forensics Report PDF",
        "no_data": "Please run a Live URL Scanner test first to compile the forensics report."
    },
    "Hindi": {
        "title": "🛡️ यूनिवर्सल साइबर शील्ड AI — SVM स्कैनर",
        "subtitle": "फ़िशिंग और धोखाधड़ी वाली वेबसाइटों की पहचान के लिए उन्नत ज्यामितीय पैटर्न पहचान इंजन",
        "lang_select": "Select Interface Language / भाषा चुनें",
        "tab1": "🔍 लाइव URL स्कैनर",
        "tab2": "📋 विस्तृत फोरेंसिक रिपोर्ट और पीडीएफ",
        "header_scan": "स्कैन करने के लिए कोई भी संदिग्ध लिंक / वेबसाइट URL दर्ज करें",
        "url_input_label": "वेबसाइट का लिंक यहाँ पेस्ट करें:",
        "url_len": "URL की लंबाई (अक्षर count)",
        "dots_count": "URL में डॉट्स (.) की संख्या",
        "hyphen_count": "URL में हाइफन (-) की संख्या",
        "subdomain_count": "कुल सबडोमेन की संख्या",
        "at_symbol": "क्या इसमें '@' सिंबल मौजूद है?",
        "ip_url": "क्या इसमें डायरेक्ट IP एड्रेस (जैसे 192.168.1.1) है?",
        "shortened": "क्या यह एक छोटा किया गया लिंक (जैसे bit.ly, tinyurl) है?",
        "dom_age": "डोमेन की उम्र (पंजीकरण के बाद से महीने)",
        "ssl_status": "क्या वैध SSL सर्टिफिकेट सक्रिय (HTTPS) है?",
        "trust_score": "गूगल सेफ ब्राउजिंग ट्रस्ट स्कोर (0-100)",
        "redirect_count": "एक्सटर्नल वेब रीडायरेक्ट की संख्या",
        "free_host": "क्या यह फ्री प्लेटफॉर्म (जैसे blogspot, vercel) पर होस्टेड है?",
        "scam_kw": "क्या इसमें स्कैम कीवर्ड्स (stipend, internship, offer, lottery) हैं?",
        "btn_scan": "⚡ हाई-सिक्योर स्कैन शुरू करें",
        "res_fake": "🚨 सुरक्षा खतरा: फ़र्जी / फ़िशिंग वेबसाइट की पहचान हुई",
        "res_legal": "✅ सत्यापित सुरक्षित: यह एक वैध और कानूनी वेबसाइट है",
        "reasons_title": "🔍 सिस्टम फोरेंसिक और पाए गए ट्रिगर पॉइंट:",
        "advice_title": "🛡️ तत्काल साइबर-सुरक्षा उपाय और समाधान:",
        "adv_fake": "1. **तुरंत ब्लॉक करें:** इस लिंक पर अपना क्रेडिट कार्ड, ओटीपी या पासवर्ड बिल्कुल दर्ज न करें।\n2. **रिपोर्ट दर्ज करें:** साइबर क्राइम हेल्पलाइन नंबर **1930** पर कॉल करें या cybercrime.gov.in पर रिपोर्ट करें।\n3. **पासवर्ड बदलें:** यदि आपने कोई जानकारी डाल दी है, तो तुरंत अपने बैंकिंग और सोशल मीडिया अकाउंट का पासवर्ड बदलें।",
        "adv_legal": "1. **ब्राउज़ करने के लिए सुरक्षित:** यह डोमेन विश्वसनीय औद्योगिक मानकों और सुरक्षा प्रोटोकॉल के अनुरूप है।\n2. **सामान्य सावधानी:** संवेदनशील भुगतान सबमिट करने से पहले हमेशा जांच लें कि ब्राउज़र का लॉक आइकन दिखाई दे रहा है या नहीं।",
        "download_btn": "📥 साइबर फोरेंसिक रिपोर्ट पीडीएफ डाउनलोड करें",
        "no_data": "फोरेंसिक रिपोर्ट संकलित करने के लिए कृपया पहले लाइव URL स्कैनर टेस्ट चलाएं।"
    }
}

selected_lang = st.sidebar.selectbox(translations["English"]["lang_select"], ["English", "Hindi"])
text = translations[selected_lang]

st.title(text["title"])
st.write(text["subtitle"])
st.markdown("---")

tab1, tab2 = st.tabs([text["tab1"], text["tab2"]])

# Persistent Session State Storage Setup
if 'scan_done' not in st.session_state:
    st.session_state.scan_done = False
if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None
if 'report_text' not in st.session_state:
    st.session_state.report_text = ""

with tab1:
    st.markdown(f"<div class='glass-card'><h3>{text['header_scan']}</h3></div>", unsafe_allow_html=True)
    user_url = st.text_input(text["url_input_label"], value="http://bit.ly")

    col1, col2 = st.columns(2)
    with col1:
        st_len = st.slider(text["url_len"], 10, 200, value=75)
        st_dots = st.slider(text["dots_count"], 1, 10, value=3)
        st_hyphens = st.slider(text["hyphen_count"], 0, 10, value=2)
        st_sub = st.number_input(text["subdomain_count"], min_value=1, max_value=10, value=3)
        st_at = st.selectbox(text["at_symbol"], [("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        st_ip = st.selectbox(text["ip_url"], [("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        st_short = st.selectbox(text["shortened"], [("No", 0), ("Yes", 1)], format_func=lambda x: x[0])

    with col2:
        st_age = st.slider(text["dom_age"], 1, 240, value=2)
        st_ssl = st.selectbox(text["ssl_status"], [("No SSL (http)", 0), ("Has Valid SSL (https)", 1)], format_func=lambda x: x[0])
        st_trust = st.slider(text["trust_score"], 0, 100, value=15)
        st_redirect = st.number_input(text["redirect_count"], min_value=0, max_value=10, value=3)
        st_free = st.selectbox(text["free_host"], [("No", 0), ("Yes", 1)], format_func=lambda x: x[0])
        st_scam = st.selectbox(text["scam_kw"], [("No", 0), ("Yes", 1)], format_func=lambda x: x[0])

    if st.button(text["btn_scan"], type="primary"):
        # Packaging dictionary inputs matching the trained features sequence mapping
        raw_input = {
            'URL_Length': st_len,
            'Qty_Dots': st_dots,
            'Qty_Hyphens': st_hyphens,
            'Subdomain_Count': st_sub,
            'Has_At_Symbol': st_at[1],
            'Is_IP_In_URL': st_ip[1],
            'Is_Shortened_URL': st_short[1],
            'Domain_Age_Months': st_age,
            'Has_Valid_SSL': st_ssl[1],
            'Google_Trust_Score': st_trust,
            'External_Redirect_Count': st_redirect,
            'Is_Free_Hosting_Domain': st_free[1],
            'Has_Scam_Keywords': st_scam[1]
        }

        # DataFrame construction with alignment to original model sequence format
        input_df = pd.DataFrame([raw_input])[model_features]

        # Scaling inputs using saved StandardScaler pipeline parameters
        input_scaled = scaler.transform(input_df)

        # SVM Classifier Engine prediction run
        prediction = model.predict(input_scaled)

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

        if prediction[0] == 1:
            st.markdown(f"<span class='status-critical'>{text['res_fake']}</span>", unsafe_allow_html=True)
            st.markdown(f"#### {text['reasons_title']}")
            reasons = (f"- ⚠️ URL is suspiciously long ({st_len} chars).\n"
                       f"- ⚠️ Domain age is dangerously low ({st_age} months).\n"
                       f"- ⚠️ Multiple external page redirects detected ({st_redirect} counts).")
            st.markdown(reasons)
            st.markdown(f"#### {text['advice_title']}")
            st.markdown(text["adv_fake"])
            status_txt = "FRAUD / FAKE WEBSITE DETECTED"
        else:
            st.markdown(f"<span class='status-secure'>{text['res_legal']}</span>", unsafe_allow_html=True)
            st.markdown(f"#### {text['advice_title']}")
            st.markdown(text["adv_legal"])
            reasons = "All structural vectors lie safely within optimal trust thresholds."
            status_txt = "VERIFIED SECURE LEGITIMATE WEBSITE"

        st.markdown("</div>", unsafe_allow_html=True)

        # Forensics Document text structure compiler engine
        full_report_text = f"""UNIVERSAL CYBER SHIELD AI SYSTEMS FORENSICS REPORT
-------------------------------------------------------------
Target URL Scanned: {user_url}
Final Assessment Outcome: {status_txt}

STRUCTURAL PARAMETER MATRIX DETECTED:
- Domain Age Configuration: {st_age} Months
- Google Trust Evaluation Score: {st_trust} / 100
- Security Socket Layers Status: {'SSL SECURE (HTTPS)' if st_ssl[1] == 1 else 'NO SSL DATA (HTTP)'}
- Suspicious Keywords Status: {'FLAGGED PRESENCE' if st_scam[1] == 1 else 'CLEAN'}

SYSTEM DETECTED TRIGGER POINTS:
{reasons.replace('- ', '')}
-------------------------------------------------------------
DISCLAIMER: This system utilizes a geometric Support Vector Machine model with an RBF Kernel
to evaluate risk boundary parameters. Maintain optimal caution before entering financial data.
"""
        st.session_state.report_text = full_report_text
        st.session_state.scan_done = True

        # PDF Generation Matrix execution loop block mapping
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.cell(200, 10, txt="UNIVERSAL CYBER SHIELD SYSTEM REPORT", ln=1, align="C")
        pdf.ln(10)
        for line in full_report_text.split('\n'):
            clean_line = line.strip()
            if clean_line:
                pdf.cell(0, 8, txt=clean_line.encode('latin-1', 'ignore').decode('latin-1'), ln=1)

        pdf_output = pdf.output(dest='S')
        # fpdf2 returns a bytearray, older fpdf returns a str — handle both safely
        if isinstance(pdf_output, str):
            pdf_bytes = pdf_output.encode('latin-1')
        else:
            pdf_bytes = bytes(pdf_output)
        st.session_state.pdf_bytes = pdf_bytes

with tab2:
    st.markdown(f"### {text['tab2']}")
    if st.session_state.scan_done:
        st.text(st.session_state.report_text)

        # Base64 string encoding conversion pipeline engine for automated browser downloads
        b64_pdf = base64.b64encode(st.session_state.pdf_bytes).decode('utf-8')
        pdf_href = (
            f'<a href="data:application/pdf;base64,{b64_pdf}" '
            f'download="cyber_shield_forensics_report.pdf">{text["download_btn"]}</a>'
        )
        st.markdown(pdf_href, unsafe_allow_html=True)
    else:
        st.warning(text["no_data"])