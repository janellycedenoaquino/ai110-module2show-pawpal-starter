import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler


def html_table(rows: list[dict]) -> str:
    """Render a list of dicts as a styled HTML table."""
    if not rows:
        return ""
    headers = list(rows[0].keys())
    th = "".join(
        f'<th style="background:#5aada0;color:#fff;font-family:\'Baloo 2\',cursive;font-weight:700;padding:8px 12px;text-align:left;font-size:.82rem;">{h}</th>'
        for h in headers
    )
    body = ""
    for i, row in enumerate(rows):
        bg = "#d4eeeb" if i % 2 == 0 else "#fffcf7"
        tds = "".join(
            f'<td style="padding:8px 12px;color:#2d4a47;font-family:\'Nunito\',sans-serif;font-size:.82rem;border-bottom:1px solid rgba(90,173,160,.15);">{v}</td>'
            for v in row.values()
        )
        body += f'<tr style="background:{bg};">{tds}</tr>'
    return f'<div style="overflow:hidden;border-radius:12px;margin-top:.6rem;"><table style="width:100%;border-collapse:collapse;"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@700;800&family=Nunito:wght@500;600;700&display=swap');

/* Page background */
[data-testid="stAppViewContainer"] {
    background-color: #edf7f5;
}
[data-testid="stHeader"] {
    background-color: #edf7f5;
}


/* Text inputs — scoped to avoid catching hidden inputs inside selectboxes */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
textarea {
    border: 2px solid #8dcec6 !important;
    border-radius: 12px !important;
    background-color: #fdf8f2 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.88rem !important;
    color: #2d4a47 !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stNumberInput"] input::placeholder,
textarea::placeholder {
    color: #8dcec6 !important;
    opacity: 1 !important;
}
/* Prevent selectbox inner input from acting like a text field */
[data-baseweb="select"] input {
    caret-color: transparent !important;
    pointer-events: none !important;
}

/* Selectbox — style the outer container, keep arrow intact */
[data-baseweb="select"] {
    border: 2px solid #8dcec6 !important;
    border-radius: 12px !important;
    background-color: #fdf8f2 !important;
}
[data-baseweb="select"] > div {
    background-color: #fdf8f2 !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.88rem !important;
    color: #2d4a47 !important;
}
/* Keep the dropdown arrow visible */
[data-baseweb="select"] svg {
    display: block !important;
    opacity: 1 !important;
    color: #3d8c80 !important;
}

/* Input labels */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: #4a7269 !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #5aada0, #3d8c80) !important;
    color: #fff !important;
    font-family: 'Baloo 2', cursive !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.45rem 1.4rem !important;
    box-shadow: 0 4px 14px rgba(61,140,128,.28) !important;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(135deg, #4a9d90, #2d7c70) !important;
}

</style>

<p style="font-family:'Baloo 2',cursive;font-weight:800;font-size:2.5rem;color:#3d8c80;line-height:1.1;margin:0;">🐾 PawPal+</p>
<p style="font-family:'Nunito',sans-serif;font-size:1.2rem;color:#7aaca5;font-weight:600;margin-top:4px;">Your pet's daily planner ✨</p>
<hr style="border:none;border-top:2px dashed #8dcec6;opacity:0.5;margin:1rem 0;">
""", unsafe_allow_html=True)

# --- Owner Setup ---
st.markdown('<span style="display:inline-flex;align-items:center;gap:5px;background:#d4eeeb;color:#3d8c80;font-family:\'Baloo 2\',cursive;font-weight:700;font-size:.72rem;padding:3px 11px;border-radius:999px;margin-bottom:.5rem;letter-spacing:.3px;text-transform:uppercase;">👤 Owner Info</span>', unsafe_allow_html=True)
owner_name = st.text_input("Owner name", value="", placeholder="e.g Janelly")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_hours=8)

st.markdown('<hr style="border:none;border-top:2px dashed #8dcec6;opacity:0.5;margin:1.2rem auto;width:40%;">', unsafe_allow_html=True)

# --- Add a Pet ---
st.markdown('<span style="display:inline-flex;align-items:center;gap:5px;background:#d4eeeb;color:#3d8c80;font-family:\'Baloo 2\',cursive;font-weight:700;font-size:.72rem;padding:3px 11px;border-radius:999px;letter-spacing:.3px;text-transform:uppercase;">🐶 Add a Pet</span>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="", placeholder="e.g Rocky")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])

if st.button("✨ Add pet"):
    if pet_name.strip() == "":
        st.warning("Please enter a pet name.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"{pet_name} added!")

if st.session_state.owner.pets:
    chips = " ".join(
        f'<span style="display:inline-flex;align-items:center;gap:4px;background:#d4eeeb;color:#3d8c80;font-family:\'Baloo 2\',cursive;font-weight:700;font-size:.78rem;padding:3px 11px 3px 8px;border-radius:999px;margin:2px;border:1.5px solid #8dcec6;">🐾 {p.name}</span>'
        for p in st.session_state.owner.pets
    )
    st.markdown(f'<div style="margin-top:.6rem">{chips}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="background:#d4eeeb;color:#2d4a47;border-left:4px solid #5aada0;border-radius:12px;padding:.65rem 1rem;font-size:.85rem;font-weight:600;margin:.5rem 0;font-family:\'Nunito\',sans-serif;">No pets yet. Add one above before adding tasks.</div>', unsafe_allow_html=True)

st.markdown('<hr style="border:none;border-top:2px dashed #8dcec6;opacity:0.5;margin:1.2rem 0;">', unsafe_allow_html=True)

# --- Add a Task ---
st.markdown('<span style="display:inline-flex;align-items:center;gap:5px;background:#d4eeeb;color:#3d8c80;font-family:\'Baloo 2\',cursive;font-weight:700;font-size:.72rem;padding:3px 11px;border-radius:999px;letter-spacing:.3px;text-transform:uppercase;">📋 Add a Task</span>', unsafe_allow_html=True)

if not st.session_state.owner.pets:
    st.markdown('<div style="background:#fad9b5;color:#5a3a10;border-left:4px solid #e8a050;border-radius:12px;padding:.65rem 1rem;font-size:.85rem;font-weight:600;margin:.5rem 0;font-family:\'Nunito\',sans-serif;">Add a pet first before adding tasks.</div>', unsafe_allow_html=True)
else:
    pet_options = [p.name for p in st.session_state.owner.pets]

    col1, col2 = st.columns([2, 1])
    with col1:
        task_title = st.text_input("Task title", value="", placeholder="e.g Walk")
    with col2:
        selected_pet = st.selectbox("Pet", pet_options)

    col3, col4, col5 = st.columns(3)
    with col3:
        duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col5:
        scheduled_time = st.text_input("Time (HH:MM)", value="08:00")

    if st.button("✨ Add task"):
        if task_title.strip() == "":
            st.markdown('<div style="background:#fad9b5;color:#2d4a47;border-left:4px solid #e8a050;border-radius:12px;padding:.65rem 1rem;font-size:.85rem;font-weight:600;margin:.5rem 0;font-family:\'Nunito\',sans-serif;">Please enter a task title.</div>', unsafe_allow_html=True)
        else:
            new_task = Task(
                title=task_title,
                duration=int(duration),
                priority=priority,
                scheduled_time=scheduled_time,
                frequency="daily"
            )
            for pet in st.session_state.owner.pets:
                if pet.name == selected_pet:
                    pet.add_task(new_task)
            st.success(f"Task '{task_title}' added to {selected_pet}!")

    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        scheduler = Scheduler(st.session_state.owner)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_pet = st.selectbox("Filter by pet", ["All"] + pet_options)
        with col_f2:
            filter_status = st.selectbox("Filter by status", ["All", "Complete", "Incomplete"])

        pet_filter = None if filter_pet == "All" else filter_pet
        status_filter = None if filter_status == "All" else (filter_status == "Complete")

        filtered = scheduler.filter_tasks(pet=pet_filter, status=status_filter)
        task_to_pet = {id(t): p.name for p in st.session_state.owner.pets for t in p.get_tasks()}

        if filtered:
            st.markdown(html_table([{
                "⏰ Time": t.scheduled_time,
                "📋 Title": t.title,
                "🐾 Pet": task_to_pet.get(id(t), "—"),
                "⏱ Mins": t.duration,
                "⚡ Priority": t.priority.capitalize(),
                "✓ Done": "✅" if t.is_complete else "—",
            } for t in filtered]), unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#d4eeeb;color:#2d4a47;border-left:4px solid #5aada0;border-radius:12px;padding:.65rem 1rem;font-size:.85rem;font-weight:600;margin:.5rem 0;font-family:\'Nunito\',sans-serif;">No tasks match the selected filter.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:#d4eeeb;color:#2d4a47;border-left:4px solid #5aada0;border-radius:12px;padding:.65rem 1rem;font-size:.85rem;font-weight:600;margin:.5rem 0;font-family:\'Nunito\',sans-serif;">No tasks yet. Add one above.</div>', unsafe_allow_html=True)

st.markdown('<hr style="border:none;border-top:2px dashed #8dcec6;opacity:0.5;margin:1.2rem 0;">', unsafe_allow_html=True)

# --- Generate Schedule ---

if st.button("🐾 Generate my schedule"):
    if not st.session_state.owner.pets:
        st.markdown('<div style="background:#fad9b5;color:#5a3a10;border-left:4px solid #e8a050;border-radius:12px;padding:.65rem 1rem;font-size:.85rem;font-weight:600;margin:.5rem 0;font-family:\'Nunito\',sans-serif;">Add a pet first.</div>', unsafe_allow_html=True)
    elif not st.session_state.owner.get_all_tasks():
        st.markdown('<div style="background:#fad9b5;color:#5a3a10;border-left:4px solid #e8a050;border-radius:12px;padding:.65rem 1rem;font-size:.85rem;font-weight:600;margin:.5rem 0;font-family:\'Nunito\',sans-serif;">Add at least one task before generating a schedule.</div>', unsafe_allow_html=True)
    else:
        scheduler = Scheduler(st.session_state.owner)
        conflicts = scheduler.detect_conflicts()
        for warning in conflicts:
            st.markdown(f'<div style="background:#fad9b5;color:#5a3a10;border-left:4px solid #e8a050;border-radius:12px;padding:.65rem 1rem;font-size:.85rem;font-weight:600;margin:.5rem 0;font-family:\'Nunito\',sans-serif;">⚠️ {warning}</div>', unsafe_allow_html=True)
        schedule = scheduler.generate_schedule()
        st.markdown(html_table([{
            "⏰ Time": t.scheduled_time,
            "📋 Task": t.title,
            "⏱ Mins": t.duration,
            "⚡ Priority": t.priority.capitalize(),
            "✓ Done": "✅" if t.is_complete else "—",
        } for t in schedule]), unsafe_allow_html=True)
