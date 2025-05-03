import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(layout="wide")
st.title("📈 UNIPOD RWANDA - PDP PROGRAM Dashboard")

# ================== CUSTOM STYLES ==================
st.markdown("""
    <style>
    .intro-badge {
        background-color: #edf6ff;
        border-left: 6px solid #1f77b4;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .intro-badge h2 {
        text-align: center;
        color: #1f77b4;
        margin-top: 0;
    }
    .intro-badge p {
        text-align: justify;
        font-size: 1.1rem;
        color: #333;
        margin: 0.5rem 0 0 0;
    }
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1.2rem;
        margin-bottom: 1.5rem;
    }
    .badge {
        background-color: #f9f9f9;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        border-radius: 12px;
        width: 15%;
        min-width: 180px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .badge h4 {
        margin: 0;
        font-size: 1rem;
        color: #333;
    }
    .badge p {
        margin: 0;
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .section-header {
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #ccc;
        padding-bottom: 0.3rem;
        color: #1f77b4;
    }
    .description-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #2ecc71;
    }
    .novelty-badge {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .progress-card {
        background: #ffffff;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid;
        box-shadow: 0 3px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .progress-card:hover {
        transform: translateY(-2px);
    }
    .progress-status {
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ================== INTRODUCTION SECTION ==================
st.markdown("""
    <div class="intro-badge">
        <h2>What is PDP?</h2>
        <p>
        The Prototype Development Program (PDP) is an initiative led by UNIPOD under the University of Rwanda.
        The program is designed to support innovators in transforming their ideas into commercially viable solutions 
        that address real community needs. Through hands-on prototyping, technical mentorship, and structured project tracking, 
        PDP empowers participants to bring their innovations to market while fostering job creation and entrepreneurship.
        </p>
    </div>
""", unsafe_allow_html=True)

# ================== LOAD DATA ==================
df = pd.read_excel("PDP-NEW.xlsx", sheet_name="PROJECTS")
df.columns = df.columns.str.strip()

status_columns = [
    "CAD Design", "PCB Design", "CAD Production", "PCB Production",
    "Backend development", "Frontend Development", "Mechanical Assembling",
    "System integration (Hardware & Software)", "Testing", "MVP", "Deploy"
]

for col in status_columns:
    if col in df.columns:
        df[col] = df[col].fillna("Not Started").str.strip()

# ================== METRICS BADGES ==================
total_projects = len(df)
cad_design_done = (df['CAD Design'] == 'Done').sum()
cad_production_done = (df['CAD Production'] == 'Done').sum()
pcb_design_done = (df['PCB Design'] == 'Done').sum()
mechanical_done = (df['Mechanical Assembling'] == 'Done').sum()
mvp_done = (df['MVP'] == 'Done').sum()

st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="badge-container">
        <div class="badge"><h4>Total Projects</h4><p>{}</p></div>
        <div class="badge"><h4>CAD Design Completed</h4><p>{}</p></div>
        <div class="badge"><h4>CAD Production Completed</h4><p>{}</p></div>
        <div class="badge"><h4>PCB Design Completed</h4><p>{}</p></div>
        <div class="badge"><h4>Mechanical Assembling Completed</h4><p>{}</p></div>
        <div class="badge"><h4>MVP Achieved</h4><p>{}</p></div>
    </div>
""".format(total_projects, cad_design_done, cad_production_done, pcb_design_done, mechanical_done, mvp_done), unsafe_allow_html=True)

# ================== VISUALIZATION 1 ==================
st.markdown('<div class="section-header">📌 Project Status Overview</div>', unsafe_allow_html=True)
status_counts = pd.melt(df[status_columns], var_name="Stage", value_name="Status")
status_summary = status_counts.groupby(["Stage", "Status"]).size().reset_index(name="Count")
fig_status = px.bar(status_summary, x="Stage", y="Count", color="Status",
                    color_discrete_map={
                        "Done": "#2ecc71", "In Progress": "#f1c40f",
                        "Not Started": "#e74c3c", "N/A": "#95a5a6"
                    },
                    title="Project Status Across Stages")
st.plotly_chart(fig_status, use_container_width=True)

# ================== VISUALIZATION 2 ==================
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="section-header">🎯 MVP Status</div>', unsafe_allow_html=True)
    if "MVP" in df.columns:
        mvp_counts = df["MVP"].value_counts().reset_index()
        mvp_counts.columns = ["Status", "Count"]
        fig_mvp = px.pie(mvp_counts, names="Status", values="Count",
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_mvp, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">📂 Project Category</div>', unsafe_allow_html=True)
    category_counts = df["Project Category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]
    fig_cat = px.pie(category_counts, names="Category", values="Count")
    st.plotly_chart(fig_cat, use_container_width=True)

# ================== RADAR CHART ==================
st.markdown('<div class="section-header">📡 Individual Project Progress Radar</div>', unsafe_allow_html=True)
projects = df["Project/Startup name"].unique()
selected_project = st.selectbox("Select Project", projects)
project_data = df[df["Project/Startup name"] == selected_project].iloc[0]
status_values = [project_data[col] for col in status_columns]
score_map = {"Done": 1.0, "In Progress": 0.5, "Not Started": 0.0, "N/A": 0.0}
scores = [score_map.get(status, 0.0) for status in status_values]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=scores,
    theta=status_columns,
    fill='toself',
    name=selected_project
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    title=f"Progress Radar for {selected_project}",
    height=500
)
st.plotly_chart(fig_radar, use_container_width=True)

# ================== DATA TABLE ==================
st.markdown('<div class="section-header">📋 All Projects Table</div>', unsafe_allow_html=True)
columns_to_display = [
    "Founder name", "Project/Startup name", "Project Category",
    "Phone", "email", "DECISION", "NOVELTY"
] + status_columns
st.dataframe(df[columns_to_display], use_container_width=True)

# ================== PROJECT DETAIL ==================
st.markdown('<div class="section-header">🔍 Project Detailed View</div>', unsafe_allow_html=True)
selected_project_detail = st.selectbox("Select Project for Details", df["Project/Startup name"].unique(), key="detail_view")
project = df[df["Project/Startup name"] == selected_project_detail].iloc[0]

# Basic Information
st.subheader("Basic Information")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**Founder:** {project['Founder name']}")
with col2:
    st.markdown(f"**Category:** {project['Project Category']}")
with col3:
    st.markdown(f"**Decision:** {project['DECISION']}")

# Project Description
st.subheader("Project Description")
st.markdown(f'<div class="description-box">{project["Project Description"]}</div>', unsafe_allow_html=True)

# Novelty Section
if pd.notna(project.get("NOVELTY")) and str(project["NOVELTY"]).strip() != "":
    st.subheader("Key Innovation")
    st.markdown(f'''
        <div class="novelty-badge">
            <h4>✨ Unique Value Proposition</h4>
            <p>{project["NOVELTY"]}</p>
        </div>
    ''', unsafe_allow_html=True)

# Contact Information
st.subheader("Contact Information")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Phone:** {project.get('Phone', 'N/A')}")
with col2:
    st.markdown(f"**Email:** {project.get('email', 'N/A')}")

# Project Progress Cards
st.subheader("Project Progress")
cols = st.columns(3)
current_col = 0

for stage in status_columns:
    status = project[stage]
    color = "#2ecc71" if status == "Done" else "#f1c40f" if status == "In Progress" else "#e74c3c"
    
    with cols[current_col]:
        st.markdown(f"""
            <div class="progress-card" style="border-color: {color}">
                <div style="font-size: 1.1rem; font-weight: 600;">{stage}</div>
                <div class="progress-status" style="color: {color}">
                    {status}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    current_col = (current_col + 1) % 3