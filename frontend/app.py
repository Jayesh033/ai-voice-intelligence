import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="Bajaj Life – AI Voice Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f0f7 100%);
    }
    
    /* Header with gradient and shadow */
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #0057b8 50%, #0074d9 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 51, 102, 0.3);
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.15rem;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
        font-weight: 500;
    }
    
    /* Beautiful cards */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 51, 102, 0.12);
        border: 1px solid rgba(0, 87, 184, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #003366 0%, #0057b8 100%);
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 87, 184, 0.2);
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.5rem;
        font-weight: 700;
        color: #003366;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid #0057b8;
    }
    
    .section-icon {
        font-size: 1.8rem;
        background: linear-gradient(135deg, #003366 0%, #0057b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Insight categories */
    .insight-category {
        background: linear-gradient(135deg, #f0f7ff 0%, #e3f2fd 100%);
        padding: 1.2rem;
        border-left: 5px solid #0057b8;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 87, 184, 0.08);
        transition: all 0.2s ease;
    }
    
    .insight-category:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0, 87, 184, 0.15);
    }
    
    .insight-category h4 {
        color: #003366;
        font-weight: 700;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
    }
    
    .insight-item {
        color: #2c3e50;
        padding: 0.4rem 0;
        padding-left: 1.5rem;
        position: relative;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .insight-item::before {
        content: '▸';
        position: absolute;
        left: 0;
        color: #0057b8;
        font-weight: bold;
    }
    
    /* Status badges */
    .status-badge {
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .badge-success {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
    }
    
    .badge-positive {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
    }
    
    .badge-negative {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
    }
    
    .badge-neutral {
        background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
        color: white;
    }
    
    .badge-connected {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
    }
    
    .badge-disconnected {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
    }
    
    /* Key phrases styling */
    .key-phrase {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        transition: all 0.2s ease;
    }
    
    .key-phrase:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Transcription box */
    .transcription-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e9ecef;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.8;
        color: #2c3e50;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.05);
        font-size: 1rem;
    }
    
    .transcription-box p {
        color: #2c3e50;
        margin: 0;
    }
    
    /* Entity badges */
    .entity-box {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border: 2px solid #e3f2fd;
        box-shadow: 0 2px 8px rgba(0, 87, 184, 0.08);
    }
    
    .entity-label {
        font-weight: 700;
        color: #003366;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .entity-value {
        color: #495057;
        font-size: 0.95rem;
    }
    
    /* Upload section */
    .upload-section {
        background: linear-gradient(135deg, #ADD8E6 0%, #f8f9fa 100%);
        padding: 2.5rem;
        border-radius: 16px;
        border: 3px dashed #0057b8;
        text-align: center;
        margin: 2rem 0;
        text-color: #003366;    
        box-shadow: 0 8px 24px rgba(0, 87, 184, 0.1);
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #003366;
        box-shadow: 0 12px 32px rgba(0, 87, 184, 0.15);
    }
    
    /* Progress bar custom styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #003366 0%, #0057b8 100%);
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.2);
        font-weight: 500;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 87, 184, 0.1);
        border: 2px solid rgba(0, 87, 184, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 87, 184, 0.2);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #003366;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animation for loading */
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .loading-shimmer {
        animation: shimmer 2s infinite linear;
        background: linear-gradient(to right, #f6f7f8 0%, #edeef1 20%, #f6f7f8 40%, #f6f7f8 100%);
        background-size: 1000px 100%;
    }
    
    /* Empty state styling */
    .empty-state {
        text-align: center;
        padding: 2rem;
        color: #6c757d;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='main-header'>
    <h1>🎙️ Bajaj Life – AI Voice Intelligence</h1>
    <p>Advanced Speech Analytics & Transcription Platform</p>
</div>
""", unsafe_allow_html=True)

# Check backend status
try:
    status_response = requests.get("http://127.0.0.1:8000/", timeout=2)
    backend_connected = True
    backend_status = "connected"
except:
    backend_connected = False
    backend_status = "disconnected"

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ System Status")
    
    if backend_connected:
        st.markdown("<span class='status-badge badge-connected'>🟢 Backend Online</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='status-badge badge-disconnected'>🔴 Backend Offline</span>", unsafe_allow_html=True)
        st.error("⚠️ Please start the backend server first!")
        st.code("uvicorn main:app --reload", language="bash")
    
    st.markdown("---")
    
    st.markdown("### 📊 Features")
    st.markdown("""
    - 🎯 **High-Accuracy Transcription**
    - 👥 **Speaker Identification**
    - 💬 **Sentiment Analysis**
    - 🏷️ **Entity Extraction**
    - 📍 **Location & Date Detection**
    - 💰 **Financial Info Extraction**
    - ✅ **Action Item Detection**
    """)
    
    st.markdown("---")
    
    st.markdown("### 📁 Supported Formats")
    st.markdown("""
    - 🎵 WAV
    - 🎧 MP3
    - 📱 M4A
    - 🎼 FLAC
    """)
    
    st.markdown("---")
    
    st.markdown("### 💡 Tips")
    st.info("For best results, use clear audio with minimal background noise and good microphone quality.")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # st.markdown("<div class='upload-section'>", unsafe_allow_html=True)
    st.markdown("### 📤 Upload Your Audio File")
    uploaded = st.file_uploader("", type=["wav", "mp3", "m4a", "flac"], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    if uploaded:
        # st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 🎵 Audio Preview")
        st.audio(uploaded, format=f"audio/{uploaded.type.split('/')[-1]}")
        st.markdown("</div>", unsafe_allow_html=True)

if uploaded:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🎯 Analyze Audio", type="primary", use_container_width=True)
    
    if analyze_button:
        if not backend_connected:
            st.error("❌ Backend server is not running. Please start it first!")
        else:
            with st.spinner("📊 Processing your audio... This may take a moment."):
                try:
                    uploaded.seek(0)
                    start_time = time.time()
                    
                    response = requests.post(
                        "http://127.0.0.1:8000/analyze",
                        files={"file": (uploaded.name, uploaded, uploaded.type)},
                        timeout=300
                    )
                    
                    elapsed_time = time.time() - start_time
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Success message
                        st.markdown(f"""
                        <div class='success-message'>
                            <strong>✅ Analysis Complete!</strong><br>
                            Processed in {elapsed_time:.1f} seconds
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Metrics row
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        
                        with metrics_col1:
                            # st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                            st.markdown("<div class='metric-value'>📝</div>", unsafe_allow_html=True)
                            word_count = len(data['transcription'].split()) if data.get('transcription') else 0
                            st.markdown(f"<div class='metric-value'>{word_count}</div>", unsafe_allow_html=True)
                            st.markdown("<div class='metric-label'>Words Transcribed</div>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with metrics_col2:
                            # st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                            st.markdown("<div class='metric-value'>🏷️</div>", unsafe_allow_html=True)
                            entity_count = sum(len(v) for v in data.get("analysis", {}).get("entities", {}).values())
                            st.markdown(f"<div class='metric-value'>{entity_count}</div>", unsafe_allow_html=True)
                            st.markdown("<div class='metric-label'>Entities Found</div>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        with metrics_col3:
                            # st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                            sentiment_label = data.get('analysis', {}).get('sentiment', {}).get('label', 'NEUTRAL')
                            sentiment_score = data.get('analysis', {}).get('sentiment', {}).get('score', 0.5)
                            sentiment_icon = "😊" if sentiment_label == "POSITIVE" else "😐" if sentiment_label == "NEUTRAL" else "😟"
                            st.markdown(f"<div class='metric-value'>{sentiment_icon}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div class='metric-value'>{sentiment_score:.0%}</div>", unsafe_allow_html=True)
                            st.markdown("<div class='metric-label'>Sentiment Score</div>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # TRANSCRIPTION
                        if data.get('transcription'):
                            # st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.markdown("<div class='section-header'><span class='section-icon'>📝</span> Full Transcription</div>", unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class='transcription-box'>
                                <p style='color: #2c3e50 !important; margin: 0; line-height: 1.8;'>{data['transcription']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # DYNAMIC INSIGHTS - Only show if data exists
                        insights_data = data.get("analysis", {}).get("dynamic_insights", {})
                        if insights_data.get("insights") and len(insights_data["insights"]) > 0:
                            # st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.markdown("<div class='section-header'><span class='section-icon'>🎯</span> Key Information Extracted</div>", unsafe_allow_html=True)
                            
                            # Create columns for insights
                            insight_cols = st.columns(2)
                            for idx, insight in enumerate(insights_data["insights"]):
                                if insight.get("items") and len(insight["items"]) > 0:
                                    with insight_cols[idx % 2]:
                                        st.markdown(f"""
                                        <div class='insight-category'>
                                            <h4>{insight.get('category', 'Information')}</h4>
                                        """, unsafe_allow_html=True)
                                        for item in insight["items"]:
                                            st.markdown(f"<div class='insight-item'>{item}</div>", unsafe_allow_html=True)
                                        st.markdown("</div>", unsafe_allow_html=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # KEY PHRASES - Only show if data exists
                        key_phrases = data.get("analysis", {}).get("key_phrases", [])
                        if key_phrases and len(key_phrases) > 0:
                            # st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.markdown("<div class='section-header'><span class='section-icon'>🔑</span> Key Phrases & Topics</div>", unsafe_allow_html=True)
                            phrases_html = "".join([f"<span class='key-phrase'>{phrase}</span>" for phrase in key_phrases])
                            st.markdown(phrases_html, unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # KEY INSIGHTS - Only show if data exists
                        key_sentences = data.get("analysis", {}).get("key_sentences", [])
                        if key_sentences and len(key_sentences) > 0:
                            # st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.markdown("<div class='section-header'><span class='section-icon'>💡</span> Key Insights</div>", unsafe_allow_html=True)
                            for idx, sentence in enumerate(key_sentences, 1):
                                st.markdown(f"""
                                <div class='insight-category'>
                                    <div class='insight-item'>{sentence}</div>
                                </div>
                                """, unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # NAMED ENTITIES - Only show if data exists
                        entities = data.get("analysis", {}).get("entities", {})
                        # Filter out empty entity lists
                        non_empty_entities = {k: v for k, v in entities.items() if v and len(v) > 0}
                        
                        if non_empty_entities:
                            # st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.markdown("<div class='section-header'><span class='section-icon'>🏷️</span> Named Entities</div>", unsafe_allow_html=True)
                            
                            entity_cols = st.columns(3)
                            entity_items = list(non_empty_entities.items())
                            
                            for idx, (entity_type, values) in enumerate(entity_items):
                                with entity_cols[idx % 3]:
                                    st.markdown(f"""
                                    <div class='entity-box'>
                                        <span class='entity-label'>{entity_type}</span>
                                        <span class='entity-value'>{', '.join(values)}</span>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                        
                        # SENTIMENT ANALYSIS - Always show
                        # st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown("<div class='section-header'><span class='section-icon'>📊</span> Sentiment Analysis</div>", unsafe_allow_html=True)
                        
                        sentiment = data.get('analysis', {}).get('sentiment', {'label': 'NEUTRAL', 'score': 0.5})
                        score = sentiment.get('score', 0.5)
                        label = sentiment.get('label', 'NEUTRAL')
                        
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            if label == "POSITIVE":
                                badge_class = "badge-positive"
                                icon = "😊"
                            elif label == "NEGATIVE":
                                badge_class = "badge-negative"
                                icon = "😟"
                            else:
                                badge_class = "badge-neutral"
                                icon = "😐"
                            
                            st.markdown(f"<div class='status-badge {badge_class}'>{icon} {label}</div>", unsafe_allow_html=True)
                        
                        with col2:
                            st.progress(score)
                            st.caption(f"Confidence Level: {score:.1%}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("""
                        ❌ **Connection Error!**
                        
                        The FastAPI backend is not running. Please start it:
                        
                        ```bash
                        uvicorn main:app --reload --host 127.0.0.1 --port 8000
                        ```
                    """)
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. The audio file might be too large or processing is taking too long.")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

else:
    # Welcome screen when no file uploaded
    # st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 3rem 0;'>
        <h2 style='color: #003366; margin-bottom: 1.5rem;'>Welcome to AI Voice Intelligence</h2>
        <p style='font-size: 1.1rem; color: #6c757d; margin-bottom: 2rem;'>
            Upload an audio file to get started with advanced speech analytics
        </p>
        <div style='display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; flex-wrap: wrap;'>
            <div style='text-align: center; min-width: 150px;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🎯</div>
                <div style='font-weight: 600; color: #003366;'>High Accuracy</div>
                <div style='color: #6c757d; font-size: 0.9rem;'>95%+ transcription accuracy</div>
            </div>
            <div style='text-align: center; min-width: 150px;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>⚡</div>
                <div style='font-weight: 600; color: #003366;'>Fast Processing</div>
                <div style='color: #6c757d; font-size: 0.9rem;'>Real-time analysis</div>
            </div>
            <div style='text-align: center; min-width: 150px;'>
                <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🔒</div>
                <div style='font-weight: 600; color: #003366;'>Secure</div>
                <div style='color: #6c757d; font-size: 0.9rem;'>Privacy protected</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center; color: #6c757d; padding: 2rem 0; font-size: 0.9rem;'>
    <p>Powered by Whisper Large-v3 & Advanced NLP | © {datetime.now().year} Bajaj Life</p>
</div>
""", unsafe_allow_html=True)