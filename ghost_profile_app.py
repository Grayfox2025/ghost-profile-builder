
# ghost_profile_app.py

import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="Ghost Profile Builder", layout="centered")

# Presets
def load_preset(preset):
    presets = {
        "Willow": {
            "Name": "Willow",
            "Age": 11,
            "Role": "ND girl with trauma",
            "Environment": "Chaotic home, distrust of adults",
            "Traits": "High IQ, Shutdown under stress, Hypervigilant, Nonlinear thinker",
            "Behaviours": "Avoids eye contact, Fixated on animals, Nightmares",
            "NeuroFlags": ["Autistic", "HSP"],
            "TraumaIndicators": "Parent conflict, Abandonment fears",
            "Mode": "Therapist"
        },
        "Ghost": {
            "Name": "Ghost",
            "Age": 43,
            "Role": "Lone wolf with trauma history",
            "Environment": "Off-grid protector, distrusts systems",
            "Traits": "Strategic, Shutdown under emotional stress, Highly moral, High IQ",
            "Behaviours": "Avoids therapy, Protective loyalty, Dreams of threat response",
            "NeuroFlags": ["Autistic", "OCD", "ADHD"],
            "TraumaIndicators": "Betrayal trauma, Loss of agency",
            "Mode": "Security"
        },
        "Mira": {
            "Name": "Mira",
            "Age": 35,
            "Role": "Trauma-affected strategist in burnout",
            "Environment": "Isolated but seeking clarity",
            "Traits": "Empathic, Overthinker, Withdraws when hurt, Deep pattern seer",
            "Behaviours": "Sleeps irregularly, Journals heavily, Emotionally intense dreams",
            "NeuroFlags": ["ADHD", "HSP"],
            "TraumaIndicators": "Emotional neglect, Loss of purpose",
            "Mode": "Self"
        }
    }
    return presets.get(preset, {})

st.title("🧠 Ghost Profile Builder")
st.subheader("Confidential Trauma-Informed Psychological Profiling Tool")

preset = st.selectbox("Load Preset", ["None", "Willow", "Ghost", "Mira"])
preset_data = load_preset(preset) if preset != "None" else {}

name = st.text_input("Name", preset_data.get("Name", ""))
age = st.number_input("Age", min_value=1, max_value=100, value=preset_data.get("Age", 25))
role = st.text_input("Role or Description", preset_data.get("Role", ""))
environment = st.text_area("Environment Description", preset_data.get("Environment", ""))
traits = st.text_area("Key Traits (comma-separated)", preset_data.get("Traits", ""))
behaviours = st.text_area("Observed Behaviours (comma-separated)", preset_data.get("Behaviours", ""))
neuroflags = st.multiselect("Neurodivergent Flags", ["Autistic", "ADHD", "OCD", "HSP", "Dyslexic"], default=preset_data.get("NeuroFlags", []))
trauma_indicators = st.text_area("Trauma Indicators (comma-separated)", preset_data.get("TraumaIndicators", ""))
mode = st.selectbox("Profile Mode", ["Parent", "Therapist", "Security", "Self"], index=["Parent", "Therapist", "Security", "Self"].index(preset_data.get("Mode", "Parent")))

def generate_profile(data):
    cognitive_style = f"- {data['Traits'][0]}, likely {data['Traits'][-1]}"
    behaviour_summary = f"- {data['Observed_Behaviours'][0]}, {data['Observed_Behaviours'][1]}"
    trauma_impact = f"- Indicators of {data['TraumaIndicators'][0]} and {data['TraumaIndicators'][1]}"
    environment_note = f"Environment described as: {data['Environment']}"
    neuro_type = f"- ND markers: {', '.join(data['NeuroFlags'])}"

    mode = data['Mode']
    if mode == "Parent":
        recs = "Recommendations for Care:\n- Use calm, sensory-friendly spaces.\n- Bond via non-verbal shared interests (e.g. animal care).\n- Introduce metaphor-rich books or shows with protector themes.\n- Avoid forced eye contact or pressure-based questioning."
    elif mode == "Therapist":
        recs = "Clinical Guidance:\n- Explore attachment wounds using safe narrative therapy.\n- Assess dissociation patterns when stressors emerge.\n- Encourage sensory grounding via animal interaction.\n- Use drawing, music, or roleplay to access pre-verbal trauma."
    elif mode == "Security":
        recs = "Operational Profile:\n- Exhibits high situational awareness and non-verbal cue reading.\n- Trust must be earned through ethical consistency.\n- Likely to perform well under high-stakes ambiguity if protected.\n- Do not rely on direct orders; use logic frameworks and mutual loyalty."
    elif mode == "Self":
        recs = "Personal Insight:\n- You protect others instinctively.\n- Your shutdowns aren’t weakness — they are tactical disengagements.\n- Structure safety as a mission, not a burden.\n- Forgive yourself for needing quiet."

    profile = f"PROFILE: {data['Name']} (Age {data['Age']}) — {data['Role']}\n\nCognitive Style:\n{cognitive_style}\n{neuro_type}\n\nBehavioural Observations:\n{behaviour_summary}\n\nTrauma & Environment:\n{trauma_impact}\n{environment_note}\n\n{recs}"
    return profile

def export_pdf(profile_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in profile_text.split("\n"):
        pdf.multi_cell(0, 10, line)
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

if st.button("Generate Profile"):
    if name and role and environment and traits and behaviours and trauma_indicators:
        data = {
            'Name': name,
            'Age': age,
            'Role': role,
            'Environment': environment,
            'Traits': [t.strip() for t in traits.split(',')],
            'Observed_Behaviours': [b.strip() for b in behaviours.split(',')],
            'NeuroFlags': neuroflags,
            'TraumaIndicators': [ti.strip() for ti in trauma_indicators.split(',')],
            'Mode': mode
        }
        profile_text = generate_profile(data)
        st.text_area("🧠 Generated Profile", profile_text, height=400)
        pdf_buffer = export_pdf(profile_text)
        st.download_button("Download PDF", pdf_buffer, file_name=f"{name}_Profile.pdf")
        st.download_button("Download as .txt", profile_text, file_name=f"{name}_Profile.txt")
    else:
        st.warning("Please fill in all required fields to generate the profile.")
