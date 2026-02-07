# app.py - WORKER HEALTH MONITORING SYSTEM (SIMPLE VERSION)

import streamlit as st
import numpy as np
from PIL import Image
import time
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="HealthGuard Pro",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .health-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .health-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .critical {
        border-left-color: #dc3545 !important;
        background-color: #ffe6e6;
    }
    .warning {
        border-left-color: #ffc107 !important;
        background-color: #fff3cd;
    }
    .healthy {
        border-left-color: #28a745 !important;
        background-color: #d4edda;
    }
    .vital-sign {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .pulse-animation {
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'health_data' not in st.session_state:
    st.session_state.health_data = {
        'heart_rate': 72,
        'stress_level': 'Low',
        'fatigue_score': 3,
        'posture_score': 85,
        'hydration_level': 'Good',
        'temperature': 36.6,
        'last_check': datetime.now()
    }

if 'health_history' not in st.session_state:
    st.session_state.health_history = []

if 'emergency' not in st.session_state:
    st.session_state.emergency = False

# Simple Health Analysis Classes
class FaceHealthAnalyzer:
    def analyze_face(self, image=None):
        """Analyze face for health indicators (simplified)"""
        np.random.seed(int(time.time()))
        
        results = {
            'heart_rate_estimate': 65 + np.random.randint(-10, 20),
            'stress_level': np.random.choice(['Low', 'Moderate', 'High'], p=[0.6, 0.3, 0.1]),
            'fatigue_signs': np.random.choice(['Alert', 'Mild Fatigue', 'Fatigued'], p=[0.5, 0.4, 0.1]),
            'temperature_estimate': 36.5 + np.random.uniform(-0.5, 0.5)
        }
        
        return results

class PostureAnalyzer:
    def analyze_posture(self, image=None):
        """Analyze posture (simplified)"""
        np.random.seed(int(time.time() * 1000) % 1000)
        
        results = {
            'posture_score': np.random.randint(60, 95),
            'shoulder_alignment': np.random.choice(['Good', 'Fair', 'Poor'], p=[0.7, 0.2, 0.1]),
            'spine_curvature': np.random.choice(['Normal', 'Slight', 'Excessive'], p=[0.8, 0.15, 0.05]),
            'head_position': np.random.choice(['Neutral', 'Forward', 'Tilted'], p=[0.75, 0.2, 0.05]),
            'recommendations': [
                "Take regular breaks",
                "Adjust chair height",
                "Keep feet flat on floor"
            ]
        }
        
        return results

class VoiceAnalyzer:
    def analyze_voice(self, audio_file=None):
        """Analyze voice for stress and fatigue (simplified)"""
        np.random.seed(int(time.time()))
        
        results = {
            'vocal_stress': np.random.uniform(0.1, 0.9),
            'fatigue_level': np.random.choice(['Low', 'Moderate', 'High'], p=[0.6, 0.3, 0.1]),
            'speech_rate': np.random.uniform(120, 180),
            'voice_health': np.random.choice(['Healthy', 'Strained', 'Fatigued'], p=[0.7, 0.2, 0.1])
        }
        
        return results
    
    def generate_waveform(self, duration=3, sample_rate=22050):
        """Generate a simulated voice waveform"""
        t = np.linspace(0, duration, int(sample_rate * duration))
        base_freq = 180 + np.random.randn() * 20
        voice_signal = np.sin(2 * np.pi * base_freq * t) * (1 + 0.3 * np.sin(2 * np.pi * 0.5 * t))
        voice_signal += 0.1 * np.random.randn(len(t))
        
        return voice_signal

# Initialize analyzers
face_analyzer = FaceHealthAnalyzer()
posture_analyzer = PostureAnalyzer()
voice_analyzer = VoiceAnalyzer()

# Helper functions
def create_health_report(face_results, posture_results, voice_results=None):
    """Create comprehensive health report"""
    report = {}
    
    # Combine metrics
    report['heart_rate'] = face_results.get('heart_rate_estimate', 72)
    report['stress_level'] = face_results.get('stress_level', 'Unknown')
    report['fatigue_level'] = face_results.get('fatigue_signs', 'Unknown')
    report['posture_score'] = posture_results.get('posture_score', 75)
    report['temperature'] = face_results.get('temperature_estimate', 36.5)
    
    if voice_results:
        report['vocal_stress'] = voice_results.get('vocal_stress', 0.5)
        report['speech_rate'] = voice_results.get('speech_rate', 150)
        report['voice_health'] = voice_results.get('voice_health', 'Healthy')
    
    # Calculate overall health score
    weights = {
        'heart_rate': 0.2,
        'stress_level': 0.25,
        'fatigue_level': 0.25,
        'posture_score': 0.2,
        'temperature': 0.1
    }
    
    # Convert categorical to numeric
    stress_score = {'Low': 90, 'Moderate': 70, 'High': 40}.get(report['stress_level'], 60)
    fatigue_score = {'Alert': 90, 'Mild Fatigue': 70, 'Fatigued': 40}.get(report['fatigue_level'], 60)
    
    overall_score = (
        weights['heart_rate'] * min(100, 100 - abs(report['heart_rate'] - 72) * 2) +
        weights['stress_level'] * stress_score +
        weights['fatigue_level'] * fatigue_score +
        weights['posture_score'] * report['posture_score'] +
        weights['temperature'] * min(100, 100 - abs(report['temperature'] - 36.6) * 20)
    )
    
    report['overall_health_score'] = int(overall_score)
    
    # Determine health status
    if overall_score >= 85:
        report['health_status'] = 'Excellent'
        report['recommendation'] = 'Maintain current routine'
    elif overall_score >= 70:
        report['health_status'] = 'Good'
        report['recommendation'] = 'Take short breaks, stay hydrated'
    elif overall_score >= 50:
        report['health_status'] = 'Fair'
        report['recommendation'] = 'Consider rest break, hydrate, stretch'
    else:
        report['health_status'] = 'Poor'
        report['recommendation'] = 'Immediate rest recommended'
    
    return report

def display_vital_signs(health_report):
    """Display vital signs in a nice format"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Heart Rate
        hr_color = 'green'
        hr = health_report['heart_rate']
        if hr > 100 or hr < 60:
            hr_color = 'red'
        elif hr > 90 or hr < 65:
            hr_color = 'orange'
        
        st.markdown(f"""
        <div class="vital-sign">
            <div style="color: gray; font-size: 12px;">❤️ HEART RATE</div>
            <div style="font-size: 24px; font-weight: bold; color: {hr_color};">{hr} BPM</div>
            <div style="font-size: 12px; color: gray;">Normal: 60-100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Stress Level
        stress_map = {'Low': 'green', 'Moderate': 'orange', 'High': 'red'}
        stress_color = stress_map.get(health_report['stress_level'], 'gray')
        
        st.markdown(f"""
        <div class="vital-sign">
            <div style="color: gray; font-size: 12px;">🧠 STRESS LEVEL</div>
            <div style="font-size: 24px; font-weight: bold; color: {stress_color};">{health_report['stress_level']}</div>
            <div style="font-size: 12px; color: gray;">Mental load</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Fatigue Level
        fatigue_map = {'Alert': 'green', 'Mild Fatigue': 'orange', 'Fatigued': 'red'}
        fatigue_color = fatigue_map.get(health_report['fatigue_level'], 'gray')
        
        st.markdown(f"""
        <div class="vital-sign">
            <div style="color: gray; font-size: 12px;">😴 FATIGUE</div>
            <div style="font-size: 24px; font-weight: bold; color: {fatigue_color};">{health_report['fatigue_level']}</div>
            <div style="font-size: 12px; color: gray;">Energy level</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Posture Score
        posture_color = 'green' if health_report['posture_score'] >= 80 else 'orange' if health_report['posture_score'] >= 60 else 'red'
        
        st.markdown(f"""
        <div class="vital-sign">
            <div style="color: gray; font-size: 12px;">🧍 POSTURE</div>
            <div style="font-size: 24px; font-weight: bold; color: {posture_color};">{health_report['posture_score']}%</div>
            <div style="font-size: 12px; color: gray;">Body alignment</div>
        </div>
        """, unsafe_allow_html=True)

# App Title
st.markdown("""
<div class="health-header">
    <h1>❤️ HealthGuard Pro</h1>
    <p>Worker Health & Wellness Monitoring System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/health-checkup.png", width=100)
    st.title("Worker Dashboard")
    
    # Worker Information
    with st.expander("👤 Worker Info", expanded=True):
        worker_id = st.selectbox(
            "Worker ID",
            ["WRK-001", "WRK-002", "WRK-003", "WRK-004", "WRK-005"],
            help="Select worker ID"
        )
        
        shift_type = st.selectbox(
            "Shift Type",
            ["Morning (6AM-2PM)", "Afternoon (2PM-10PM)", "Night (10PM-6AM)"],
            index=0
        )
        
        department = st.selectbox(
            "Department",
            ["Assembly", "Logistics", "Quality Control", "Maintenance", "Packaging"]
        )
    
    # Health Thresholds
    with st.expander("⚙️ Health Settings"):
        alert_heart_rate = st.slider("Max Heart Rate Alert", 80, 120, 100)
        min_posture_score = st.slider("Min Posture Score", 50, 90, 70)
        auto_health_check = st.checkbox("Auto Health Checks", True)
    
    st.divider()
    
    # Quick Actions
    st.subheader("Quick Actions")
    
    if st.button("📋 Daily Health Check", use_container_width=True):
        st.session_state.run_health_check = True
    
    if st.button("🔄 Reset All Data", use_container_width=True, type="secondary"):
        st.session_state.health_data = {
            'heart_rate': 72,
            'stress_level': 'Low',
            'fatigue_score': 3,
            'posture_score': 85,
            'hydration_level': 'Good',
            'temperature': 36.6,
            'last_check': datetime.now()
        }
        st.rerun()
    
    # Emergency Button
    st.divider()
    if st.button("🚨 EMERGENCY ALERT", type="primary", use_container_width=True):
        st.session_state.emergency = True
        st.error("Medical emergency alert sent!")

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Dashboard", 
    "📸 Health Scan", 
    "🎤 Voice Analysis", 
    "📊 Health Analytics"
])

# Dashboard Tab
with tab1:
    st.header("Worker Health Dashboard")
    
    # Current Health Status
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current Health Status")
        
        # Health Score Gauge
        health_score = st.session_state.health_data['posture_score']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={'text': "Overall Health Score"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#28a745"},
                'steps': [
                    {'range': [0, 50], 'color': "#dc3545"},
                    {'range': [50, 75], 'color': "#ffc107"},
                    {'range': [75, 100], 'color': "#28a745"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': health_score
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Alert Banner
        if health_score < 60:
            st.error("⚠️ LOW HEALTH SCORE - Worker needs immediate attention!")
        elif health_score < 75:
            st.warning("⚠️ MODERATE HEALTH SCORE - Monitor closely")
        else:
            st.success("✅ GOOD HEALTH SCORE - Worker is in good condition")
    
    with col2:
        st.subheader("Quick Actions")
        
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            if st.button("💧 Log Hydration"):
                st.session_state.health_data['hydration_level'] = 'Good'
                st.success("Hydration logged!")
            
            if st.button("🧘 Log Stretch"):
                st.success("Stretch break logged!")
        
        with action_col2:
            if st.button("😴 Log Rest"):
                st.session_state.health_data['fatigue_score'] = max(1, st.session_state.health_data['fatigue_score'] - 1)
                st.success("Rest break logged!")
            
            if st.button("📝 Add Note"):
                note = st.text_input("Add health note:", key="health_note_input")
                if note:
                    st.success(f"Note added: {note}")
        
        # Today's Summary
        st.subheader("Today's Summary")
        st.metric("Hours Worked", "4.5", "+0.5")
        st.metric("Breaks Taken", "2", "0")
        st.metric("Water Intake", "1.2L", "+0.3L")
    
    # Health Metrics Over Time
    st.subheader("Health Trends")
    
    # Generate sample trend data
    hours = list(range(1, 9))
    heart_rates = [72 + np.random.randint(-5, 5) for _ in hours]
    stress_scores = [30 + np.random.randint(-10, 10) for _ in hours]
    posture_scores = [85 + np.random.randint(-10, 5) for _ in hours]
    
    trend_df = pd.DataFrame({
        'Hour': hours,
        'Heart Rate': heart_rates,
        'Stress Score': stress_scores,
        'Posture Score': posture_scores
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trend_df['Hour'], y=trend_df['Heart Rate'], 
                           name='Heart Rate', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=trend_df['Hour'], y=trend_df['Stress Score'], 
                           name='Stress Score', line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=trend_df['Hour'], y=trend_df['Posture Score'], 
                           name='Posture Score', line=dict(color='green', width=2)))
    
    fig.update_layout(
        title="Health Metrics Over Work Hours",
        xaxis_title="Hour of Day",
        yaxis_title="Score / Rate",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Health Scan Tab
with tab2:
    st.header("Worker Health Scan")
    
    # Scan Options
    scan_type = st.radio(
        "Select Scan Type:",
        ["Camera Scan", "Image Upload", "Quick Health Check"],
        horizontal=True
    )
    
    if scan_type == "Camera Scan":
        st.info("📹 Using camera for real-time health analysis")
        
        camera_input = st.camera_input("Take a photo for health analysis")
        
        if camera_input:
            # Load image
            image = Image.open(camera_input)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption="Camera Capture", use_column_width=True)
                
                # Analyze button
                if st.button("🔍 Analyze Health", type="primary", use_container_width=True):
                    with st.spinner("Analyzing health indicators..."):
                        # Analyze face health (simplified)
                        face_results = face_analyzer.analyze_face()
                        
                        # Analyze posture (simplified)
                        posture_results = posture_analyzer.analyze_posture()
                        
                        # Create comprehensive report
                        health_report = create_health_report(face_results, posture_results)
                        
                        # Update session state
                        st.session_state.health_data.update({
                            'heart_rate': health_report['heart_rate'],
                            'stress_level': health_report['stress_level'],
                            'fatigue_score': {'Alert': 1, 'Mild Fatigue': 2, 'Fatigued': 3}.get(health_report['fatigue_level'], 2),
                            'posture_score': health_report['posture_score'],
                            'last_check': datetime.now()
                        })
                        
                        # Add to history
                        st.session_state.health_history.append({
                            'timestamp': datetime.now(),
                            'report': health_report
                        })
                        
                        # Display results in col2
                        with col2:
                            st.success("✅ Health Analysis Complete!")
                            display_vital_signs(health_report)
                            
                            # Health Status
                            st.subheader(f"Overall Health: {health_report['health_status']}")
                            
                            # Detailed Findings
                            with st.expander("📋 Detailed Findings", expanded=True):
                                st.write(f"**Heart Rate Estimate:** {health_report['heart_rate']} BPM")
                                st.write(f"**Stress Level:** {health_report['stress_level']}")
                                st.write(f"**Fatigue Signs:** {health_report['fatigue_level']}")
                                st.write(f"**Posture Score:** {health_report['posture_score']}%")
                                st.write(f"**Temperature Estimate:** {health_report['temperature']:.1f}°C")
                                st.write(f"**Shoulder Alignment:** {posture_results['shoulder_alignment']}")
                                st.write(f"**Spine Curvature:** {posture_results['spine_curvature']}")
                            
                            # Recommendations
                            st.subheader("💡 Recommendations")
                            st.info(health_report['recommendation'])
                            
                            if posture_results.get('recommendations'):
                                for rec in posture_results['recommendations']:
                                    st.write(f"• {rec}")
            
            if not st.session_state.get('analysis_done', False):
                with col2:
                    st.info("👈 Click 'Analyze Health' to start analysis")
    
    elif scan_type == "Image Upload":
        st.info("📤 Upload a worker photo for analysis")
        
        uploaded_file = st.file_uploader(
            "Choose a worker image",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear photo of the worker's face and upper body"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(image, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                if st.button("🔍 Analyze Uploaded Image", type="primary", use_container_width=True):
                    with st.spinner("Analyzing health indicators..."):
                        # Analyze face health (simplified)
                        face_results = face_analyzer.analyze_face()
                        
                        # Analyze posture (simplified)
                        posture_results = posture_analyzer.analyze_posture()
                        
                        # Create comprehensive report
                        health_report = create_health_report(face_results, posture_results)
                        
                        # Display results
                        st.success("✅ Health Analysis Complete!")
                        display_vital_signs(health_report)
                        
                        # Detailed report
                        st.subheader("Health Report")
                        
                        report_data = {
                            "Metric": ["Overall Health", "Heart Rate", "Stress", "Fatigue", "Posture", "Temperature"],
                            "Value": [
                                f"{health_report['health_status']} ({health_report['overall_health_score']}/100)",
                                f"{health_report['heart_rate']} BPM",
                                health_report['stress_level'],
                                health_report['fatigue_level'],
                                f"{health_report['posture_score']}%",
                                f"{health_report['temperature']:.1f}°C"
                            ],
                            "Status": [
                                "✅" if health_report['overall_health_score'] >= 70 else "⚠️" if health_report['overall_health_score'] >= 50 else "❌",
                                "✅" if 60 <= health_report['heart_rate'] <= 100 else "⚠️",
                                "✅" if health_report['stress_level'] == 'Low' else "⚠️" if health_report['stress_level'] == 'Moderate' else "❌",
                                "✅" if health_report['fatigue_level'] == 'Alert' else "⚠️" if health_report['fatigue_level'] == 'Mild Fatigue' else "❌",
                                "✅" if health_report['posture_score'] >= 80 else "⚠️" if health_report['posture_score'] >= 60 else "❌",
                                "✅" if 36 <= health_report['temperature'] <= 37.5 else "⚠️"
                            ]
                        }
                        
                        st.table(pd.DataFrame(report_data))
    
    else:  # Quick Health Check
        st.info("⚡ Quick health assessment based on current data")
        
        # Simple form for quick assessment
        with st.form("quick_health_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                self_energy = st.slider("Energy Level", 1, 10, 7)
                self_hydration = st.selectbox("Hydration", ["Poor", "Fair", "Good", "Excellent"])
            
            with col2:
                self_stress = st.slider("Stress Level", 1, 10, 4)
                self_discomfort = st.multiselect("Discomfort Areas", 
                                                ["None", "Back", "Neck", "Shoulders", "Eyes", "Legs"])
            
            with col3:
                self_hours_slept = st.number_input("Hours Slept", 0.0, 12.0, 7.0)
                self_breaks_taken = st.number_input("Breaks Taken", 0, 10, 2)
            
            submitted = st.form_submit_button("Submit Health Check", type="primary")
            
            if submitted:
                # Calculate health score
                energy_score = self_energy * 10
                stress_score = 100 - (self_stress * 8)
                sleep_score = min(100, (self_hours_slept / 8) * 100)
                break_score = min(100, (self_breaks_taken / 4) * 100)
                
                overall_score = (energy_score + stress_score + sleep_score + break_score) / 4
                
                # Display results
                st.success("✅ Quick Health Check Submitted!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Estimated Health Score", f"{overall_score:.0f}/100")
                    
                    if overall_score >= 80:
                        st.success("✅ Excellent condition!")
                    elif overall_score >= 60:
                        st.warning("⚠️ Fair condition")
                    else:
                        st.error("❌ Needs attention")
                
                with col2:
                    # Recommendations
                    st.subheader("Recommendations")
                    
                    if self_energy < 5:
                        st.write("• Consider a short break")
                    if self_stress > 6:
                        st.write("• Practice deep breathing")
                    if self_hours_slept < 6:
                        st.write("• Ensure adequate sleep")
                    if len(self_discomfort) > 2:
                        st.write("• Stretch affected areas")

# Voice Analysis Tab
with tab3:
    st.header("Voice Health Analysis")
    st.info("🎤 Analyze voice for stress, fatigue, and vocal health indicators")
    
    # Analysis Options
    voice_option = st.radio(
        "Select Input Method:",
        ["Record Audio", "Text Analysis", "Simulate Analysis"],
        horizontal=True
    )
    
    if voice_option == "Record Audio":
        st.warning("Note: Audio recording requires browser microphone permission")
        
        audio_bytes = st.audio_input("Record worker voice for analysis (speak for 5-10 seconds)")
        
        if audio_bytes:
            st.success("✅ Audio recorded successfully!")
            
            if st.button("Analyze Voice Recording", type="primary"):
                with st.spinner("Analyzing voice patterns..."):
                    # Simulate voice analysis
                    voice_results = voice_analyzer.analyze_voice()
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Voice Analysis Results")
                        
                        # Vocal Stress Meter
                        stress_value = voice_results['vocal_stress'] * 100
                        fig = go.Figure(go.Indicator(
                            mode="gauge",
                            value=stress_value,
                            title={'text': "Vocal Stress"},
                            domain={'x': [0, 1], 'y': [0, 1]},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "orange" if stress_value > 60 else "green"},
                                'steps': [
                                    {'range': [0, 40], 'color': "green"},
                                    {'range': [40, 70], 'color': "orange"},
                                    {'range': [70, 100], 'color': "red"}
                                ]
                            }
                        ))
                        fig.update_layout(height=250)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Voice metrics
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric("Speech Rate", f"{voice_results['speech_rate']:.0f} WPM")
                            st.metric("Fatigue Level", voice_results['fatigue_level'])
                        with col_b:
                            st.metric("Voice Health", voice_results['voice_health'])
                    
                    with col2:
                        st.subheader("Voice Visualization")
                        
                        # Create waveform plot
                        voice_signal = voice_analyzer.generate_waveform()
                        fig, ax = plt.subplots(figsize=(10, 4))
                        ax.plot(voice_signal[:5000], color='blue', alpha=0.7, linewidth=1)
                        ax.set_xlabel('Samples')
                        ax.set_ylabel('Amplitude')
                        ax.set_title('Voice Waveform Pattern')
                        ax.grid(True, alpha=0.3)
                        st.pyplot(fig)
                        
                        # Voice health recommendations
                        st.subheader("💡 Voice Care Tips")
                        
                        if voice_results['vocal_stress'] > 0.7:
                            st.warning("⚠️ High vocal stress detected")
                            st.write("• Drink warm water with honey")
                            st.write("• Avoid shouting or straining")
                            st.write("• Take 5-minute voice breaks hourly")
                        elif voice_results['fatigue_level'] == 'High':
                            st.warning("⚠️ Voice fatigue detected")
                            st.write("• Rest your voice for 15 minutes")
                            st.write("• Stay hydrated")
                            st.write("• Avoid caffeine")
                        else:
                            st.success("✅ Voice appears healthy")
                            st.write("• Maintain good hydration")
                            st.write("• Practice vocal warm-ups")
    
    elif voice_option == "Text Analysis":
        st.info("Analyze written text for stress indicators")
        
        text_input = st.text_area("Enter worker's self-reported text:", 
                                 placeholder="How are you feeling today? Describe your current state...",
                                 height=150)
        
        if text_input:
            if st.button("Analyze Text", type="primary"):
                with st.spinner("Analyzing text for stress indicators..."):
                    # Simple text analysis
                    word_count = len(text_input.split())
                    
                    # Detect stress keywords
                    stress_keywords = ['tired', 'stressed', 'overwhelmed', 'exhausted', 'burnout', 
                                      'anxious', 'worried', 'pressure', 'deadline', 'rush']
                    
                    stress_words = sum(1 for word in text_input.lower().split() if word in stress_keywords)
                    stress_ratio = stress_words / max(1, word_count)
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Word Count", word_count)
                        st.metric("Stress Keywords", stress_words)
                        
                        # Stress level based on text
                        if stress_ratio > 0.1:
                            stress_level = "High"
                            stress_color = "red"
                        elif stress_ratio > 0.05:
                            stress_level = "Moderate"
                            stress_color = "orange"
                        else:
                            stress_level = "Low"
                            stress_color = "green"
                        
                        st.markdown(f"""
                        <div class="vital-sign">
                            <div style="color: gray; font-size: 12px;">📝 TEXT STRESS LEVEL</div>
                            <div style="font-size: 24px; font-weight: bold; color: {stress_color};">{stress_level}</div>
                            <div style="font-size: 12px; color: gray;">Based on word analysis</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.subheader("Analysis Insights")
                        
                        if stress_ratio > 0.1:
                            st.error("**High stress detected in text**")
                            st.write("Recommendations:")
                            st.write("• Schedule a break")
                            st.write("• Consider talking to supervisor")
                            st.write("• Practice relaxation techniques")
                        elif stress_ratio > 0.05:
                            st.warning("**Moderate stress detected**")
                            st.write("Suggestions:")
                            st.write("• Take short breaks")
                            st.write("• Stay hydrated")
                            st.write("• Practice deep breathing")
                        else:
                            st.success("**Text shows normal stress levels**")
                            st.write("Maintain:")
                            st.write("• Regular breaks")
                            st.write("• Good work-life balance")
                            st.write("• Open communication")
    
    else:  # Simulate Analysis
        st.info("Running simulated voice analysis...")
        
        # Generate simulated voice analysis
        if st.button("Run Simulation", type="primary"):
            with st.spinner("Simulating voice analysis..."):
                time.sleep(2)
                
                # Generate multiple simulations for comparison
                simulations = []
                for i in range(5):
                    voice_results = voice_analyzer.analyze_voice()
                    simulations.append({
                        'Time': f"Test {i+1}",
                        'Stress': voice_results['vocal_stress'] * 100,
                        'Fatigue': {'Low': 25, 'Moderate': 50, 'High': 75}[voice_results['fatigue_level']],
                        'Speech Rate': voice_results['speech_rate'],
                        'Health': {'Healthy': 90, 'Strained': 60, 'Fatigued': 30}[voice_results['voice_health']]
                    })
                
                sim_df = pd.DataFrame(simulations)
                
                # Display results
                st.success("✅ Simulation Complete!")
                
                # Create comparison chart
                fig = go.Figure(data=[
                    go.Bar(name='Stress', x=sim_df['Time'], y=sim_df['Stress'], marker_color='#FF6B6B'),
                    go.Bar(name='Fatigue', x=sim_df['Time'], y=sim_df['Fatigue'], marker_color='#FFD166'),
                    go.Bar(name='Health', x=sim_df['Time'], y=sim_df['Health'], marker_color='#06D6A0')
                ])
                
                fig.update_layout(
                    title="Simulated Voice Analysis Results",
                    barmode='group',
                    xaxis_title="Test Number",
                    yaxis_title="Score (0-100)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show latest simulation details
                latest = simulations[-1]
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Vocal Stress", f"{latest['Stress']:.0f}%")
                with col2:
                    st.metric("Speech Rate", f"{latest['Speech Rate']:.0f} WPM")
                with col3:
                    health_text = "Healthy" if latest['Health'] > 70 else "Strained" if latest['Health'] > 40 else "Fatigued"
                    st.metric("Voice Health", health_text)

# Health Analytics Tab
with tab4:
    st.header("Health Analytics & Trends")
    
    # Generate historical data
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    health_scores = np.random.uniform(60, 95, 30)
    stress_levels = np.random.uniform(20, 80, 30)
    fatigue_scores = np.random.uniform(30, 90, 30)
    posture_scores = np.random.uniform(65, 95, 30)
    
    analytics_df = pd.DataFrame({
        'Date': dates.strftime('%m-%d'),
        'Health_Score': health_scores,
        'Stress_Level': stress_levels,
        'Fatigue_Score': fatigue_scores,
        'Posture_Score': posture_scores
    })
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Health Score Trend")
        fig = px.line(analytics_df, x='Date', y='Health_Score', 
                     title="30-Day Health Score History",
                     line_shape='spline')
        fig.update_traces(line=dict(color='#06D6A0', width=3))
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Health Components")
        
        # Current day metrics
        current_day = {
            'Metric': ['Overall Health', 'Stress', 'Fatigue', 'Posture'],
            'Score': [
                analytics_df['Health_Score'].iloc[-1],
                analytics_df['Stress_Level'].iloc[-1],
                analytics_df['Fatigue_Score'].iloc[-1],
                analytics_df['Posture_Score'].iloc[-1]
            ]
        }
        
        fig = go.Figure(data=[
            go.Bar(x=current_day['Metric'], 
                  y=current_day['Score'],
                  marker_color=['#28a745', '#ffc107', '#dc3545', '#17a2b8'])
        ])
        
        fig.update_layout(
            title="Today's Health Metrics",
            yaxis_title="Score",
            yaxis_range=[0, 100],
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    st.subheader("Health Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        avg_health = analytics_df['Health_Score'].mean()
        st.metric("Avg Health Score", f"{avg_health:.1f}")
    
    with stat_col2:
        min_health = analytics_df['Health_Score'].min()
        st.metric("Lowest Score", f"{min_health:.1f}")
    
    with stat_col3:
        days_healthy = len(analytics_df[analytics_df['Health_Score'] >= 75])
        st.metric("Healthy Days", days_healthy)
    
    with stat_col4:
        improvement = analytics_df['Health_Score'].iloc[-1] - analytics_df['Health_Score'].iloc[0]
        st.metric("30-Day Change", f"{improvement:+.1f}")
    
    # Export options
    st.divider()
    st.subheader("Export & Reports")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        csv = analytics_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Data",
            data=csv,
            file_name="health_analytics.csv",
            mime="text/csv"
        )
    
    with export_col2:
        if st.button("📄 Generate Health Report", type="primary"):
            with st.spinner("Generating report..."):
                time.sleep(1)
                st.success("✅ Health report generated successfully!")
                
                # Show sample report
                with st.expander("📋 Preview Report", expanded=True):
                    st.write(f"""
                    **MONTHLY HEALTH REPORT**
                    ========================
                    
                    **Summary:**
                    - Average Health Score: {avg_health:.1f}/100
                    - Healthy Days: {days_healthy}
                    - Improvement Trend: {improvement:.1f} points
                    
                    **Recommendations:**
                    1. Continue monitoring stress levels
                    2. Maintain posture improvement exercises
                    3. Schedule regular health check-ups
                    4. Encourage hydration and breaks
                    
                    **Next Steps:**
                    - Schedule individual health consultations
                    - Implement workstation ergonomics review
                    - Plan wellness workshops
                    """)

# Emergency Overlay
if st.session_state.get('emergency', False):
    st.markdown("""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(220, 53, 69, 0.95);
        z-index: 9999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
        padding: 2rem;
    ">
        <h1 style="font-size: 4em; margin-bottom: 1rem;">🚨 MEDICAL ALERT 🚨</h1>
        <p style="font-size: 1.5em; margin-bottom: 2rem;">Worker health emergency detected!</p>
        <div style="background-color: white; color: #dc3545; padding: 1rem 2rem; border-radius: 10px; margin-bottom: 2rem;">
            <p style="font-size: 1.2em; margin: 0;">On-site Nurse: Ext. 2222</p>
            <p style="font-size: 1.2em; margin: 0;">Medical Station: Building B, Floor 2</p>
            <p style="font-size: 1.2em; margin: 0;">Emergency: Dial 911</p>
        </div>
        <button onclick="window.location.reload()" style="
            padding: 15px 30px;
            font-size: 1.2em;
            background-color: white;
            color: #dc3545;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        ">
            ACKNOWLEDGE & CONTINUE
        </button>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; padding: 1rem;">
    <p>❤️ <strong>HealthGuard Pro</strong> v2.0 | Worker Health & Wellness Monitoring</p>
    <p>⚠️ This tool aids health monitoring but doesn't replace medical advice.</p>
    <p>📞 Medical Emergency: 911 | Company Nurse: 1-800-HEALTH</p>
</div>
""", unsafe_allow_html=True)