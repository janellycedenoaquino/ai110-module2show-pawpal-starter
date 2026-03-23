import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

# --- Owner Setup ---
st.subheader("Owner Info")
owner_name = st.text_input("Owner name", value="")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_hours=8)

# --- Add a Pet ---
st.subheader("Add a Pet")
col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])

if st.button("Add pet"):
    if pet_name.strip() == "":
        st.warning("Please enter a pet name.")
    else:
        new_pet = Pet(name=pet_name, species=species)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"{pet_name} added!")

# Show current pets
if st.session_state.owner.pets:
    st.write("Your pets:", [p.name for p in st.session_state.owner.pets])
else:
    st.info("No pets yet. Add one above before adding tasks.")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

if not st.session_state.owner.pets:
    st.warning("Add a pet first before adding tasks.")
else:
    pet_options = [p.name for p in st.session_state.owner.pets]
    selected_pet = st.selectbox("Select pet", pet_options)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="")
    with col2:
        duration = st.number_input("Duration (mins)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        scheduled_time = st.text_input("Time (HH:MM)", value="08:00")

    if st.button("Add task"):
        if task_title.strip() == "":
            st.warning("Please enter a task title.")
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

    # Show current tasks
    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table([{
            "Title": t.title,
            "Pet": selected_pet,
            "Time": t.scheduled_time,
            "Duration": t.duration,
            "Priority": t.priority,
            "Done": t.is_complete
        } for t in all_tasks])
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    if not st.session_state.owner.pets:
        st.warning("Add a pet first.")
    elif not st.session_state.owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(f"⚠️ {warning}")
        schedule = scheduler.generate_schedule()
        st.success("Here is today's schedule:")
        st.table([{
            "Time": t.scheduled_time,
            "Task": t.title,
            "Duration (mins)": t.duration,
            "Priority": t.priority,
            "Done": t.is_complete
        } for t in schedule])
