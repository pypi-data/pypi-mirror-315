import streamlit as st
from my_component import kanban

if "kanban_data" not in st.session_state:
    st.session_state.kanban_data = {
        "columns": [
            {
                "id": "todo",
                "title": "To Do",
                "cards": [
                    {"id": "card-1", "name": "Task 1", "fields": ["Bug"], "color": "#FF5555"},
                    {"id": "card-2", "name": "Task 2", "fields": ["Bug"], "color": "#55FF55"},
                ],
            },
            {
                "id": "in-progress",
                "title": "In Progress",
                "cards": [
                    {"id": "card-3", "name": "Task 3", "fields": ["Bug"], "color": "#5555FF"},
                ],
            },
            {"id": "done", "title": "Done", "cards": []},
        ]
    }

updated_data = kanban(columns=st.session_state.kanban_data["columns"], key="kanban")

# Debugging: Log the returned data
st.write("Returned Data from Kanban Component:")
st.write(updated_data)

if updated_data:
    # Update session state only if data is returned
    st.session_state.kanban_data["columns"] = updated_data["columns"]