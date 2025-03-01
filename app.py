import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit page configuration
st.set_page_config(
    page_title="Delhivery Logistics Analysis",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .main {
        background-color: #1e1e1e;
        padding: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .header {
        color: #e0e0e0;
        font-family: 'Arial', sans-serif;
    }
    .metric-card {
        background-color: #2c2c2c;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        color: #e0e0e0;
    }
    h1, h2, h3, p {
        color: #e0e0e0;
    }
    .stDataFrame {
        background-color: #2c2c2c;
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and header
st.title("Delhivery Logistics & Shipment Data Analysis 📦")
st.markdown("<h3 class='header'>Real-time Delivery Insights</h3>", unsafe_allow_html=True)

# Sidebar for additional controls
with st.sidebar:
    st.header("Analysis Controls")
    st.info("Click the button below to load the Delhivery dataset")
    
    if st.button("Load Delhivery Dataset"):
        try:
            df = pd.read_csv("delhivery_data.csv")
            st.session_state['df'] = df
            st.success("Dataset loaded successfully!")
        except FileNotFoundError:
            st.error("Error: 'delhivery_data.csv' not found. Please ensure the file is in the working directory.")

# Main content
if 'df' in st.session_state:
    df = st.session_state['df']
    
    # Key Metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Shipments", len(df))
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Avg Actual Time", f"{df['actual_time'].mean():.1f} min")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Avg OSRM Time", f"{df['osrm_time'].mean():.1f} min")
        st.markdown("</div>", unsafe_allow_html=True)

    # Data Preview
    st.subheader("Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Visualization Section
    st.subheader("Delivery Time Analysis")

    # KDE Plot
    st.markdown("### Actual vs Predicted Time (KDE Plot)")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.kdeplot(data=df, x='actual_time', label='Actual Time', fill=True, color='#00b4d8', alpha=0.6)
    sns.kdeplot(data=df, x='osrm_time', label='OSRM Predicted Time', fill=True, color='#ff6b6b', alpha=0.6)
    ax1.set_xlabel("Time (Minutes)", fontsize=12, color='#e0e0e0')
    ax1.set_ylabel("Density", fontsize=12, color='#e0e0e0')
    ax1.set_title("Actual vs Predicted Delivery Time", fontsize=14, pad=15, color='#e0e0e0')
    ax1.legend()
    ax1.grid(True, alpha=0.2)
    ax1.set_facecolor('#2c2c2c')
    fig1.set_facecolor('#1e1e1e')
    ax1.tick_params(colors='#e0e0e0')
    plt.style.use('seaborn-v0_8-dark')
    st.pyplot(fig1)

    # Bar Plot (assuming a categorical column like 'route_type' exists)
    if 'route_type' in df.columns:
        st.markdown("### Shipments by Route Type (Bar Plot)")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, x='route_type', palette='viridis')
        ax2.set_xlabel("Route Type", fontsize=12, color='#e0e0e0')
        ax2.set_ylabel("Number of Shipments", fontsize=12, color='#e0e0e0')
        ax2.set_title("Shipments by Route Type", fontsize=14, pad=15, color='#e0e0e0')
        ax2.set_facecolor('#2c2c2c')
        fig2.set_facecolor('#1e1e1e')
        ax2.tick_params(colors='#e0e0e0')
        plt.style.use('seaborn-v0_8-dark')
        st.pyplot(fig2)

    # Box Plot
    st.markdown("### Time Distribution (Box Plot)")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df[['actual_time', 'osrm_time']], palette='Set2')
    ax3.set_ylabel("Time (Minutes)", fontsize=12, color='#e0e0e0')
    ax3.set_title("Distribution of Actual and Predicted Times", fontsize=14, pad=15, color='#e0e0e0')
    ax3.set_facecolor('#2c2c2c')
    fig3.set_facecolor('#1e1e1e')
    ax3.tick_params(colors='#e0e0e0')
    plt.style.use('seaborn-v0_8-dark')
    st.pyplot(fig3)

    # Scatter Plot
    st.markdown("### Actual vs Predicted Time (Scatter Plot)")
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='osrm_time', y='actual_time', hue='actual_time', palette='coolwarm', alpha=0.6)
    ax4.set_xlabel("OSRM Predicted Time (Minutes)", fontsize=12, color='#e0e0e0')
    ax4.set_ylabel("Actual Time (Minutes)", fontsize=12, color='#e0e0e0')
    ax4.set_title("Actual vs Predicted Time Correlation", fontsize=14, pad=15, color='#e0e0e0')
    ax4.grid(True, alpha=0.2)
    ax4.set_facecolor('#2c2c2c')
    fig4.set_facecolor('#1e1e1e')
    ax4.tick_params(colors='#e0e0e0')
    plt.style.use('seaborn-v0_8-dark')
    st.pyplot(fig4)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Aditya Upadhyay | Delhivery Logistics Analysis</p>", 
           unsafe_allow_html=True)