import streamlit as st
from datetime import datetime, timedelta

# Ensure 'people' is correctly initialized as a dictionary in session state
if 'people' not in st.session_state or not isinstance(st.session_state.people, dict):
    st.session_state.people = {}

def calculate_days_until_next_birthday(birthday, today):
    """Calculate days until the next birthday."""
    next_year = today.year + (today >= birthday.replace(year=today.year))
    next_birthday = birthday.replace(year=next_year)
    return (next_birthday - today).days

def adjust_to_nearest_saturday(plan_date):
    """Adjust to the nearest Saturday unless within specified holiday periods."""
    if (plan_date.month == 5 and 1 <= plan_date.day <= 3) or (plan_date.month == 10 and 1 <= plan_date.day <= 7):
        return plan_date, "It's a holiday period, so no adjustment is made."
    
    if plan_date.weekday() in [0, 1]:  # Monday or Tuesday
        adjusted_date = plan_date - timedelta(days=plan_date.weekday() + 1)
        adjustment_message = "It's a weekday, adjusted to the previous Saturday."
    elif 2 <= plan_date.weekday() <= 4:  # Wednesday to Friday
        adjusted_date = plan_date + timedelta(days=5 - plan_date.weekday())
        adjustment_message = "It's a weekday, adjusted to the next Saturday."
    else:
        adjusted_date = plan_date
        adjustment_message = "It's already a weekend, no adjustment needed."
    return adjusted_date, adjustment_message

def main():
    st.title("🎉 Birthday Party Planner")
    
    with st.form("person_form"):
        name = st.text_input("Name").strip()
        relationship = st.selectbox("Relationship", ["Father", "Mother", "Grandfather", "Grandmother", "Girlfriend", "Classmate", "Friend", "Other"])
        birthday = st.date_input("Birthday")
        submit_button = st.form_submit_button(label="Save or Update")

    if submit_button and name:
        st.session_state.people[name] = {
            "relationship": relationship,
            "birthday": birthday,
        }
        st.success(f"{name}'s information saved/updated!")

    if st.session_state.people:
        selected_person = st.selectbox("Select a person to plan a birthday for", options=list(st.session_state.people.keys()))
        
        if selected_person:
            person_info = st.session_state.people[selected_person]
            st.write(f"Name: {selected_person}, Relationship: {person_info['relationship']}, Birthday: {person_info['birthday'].strftime('%Y-%m-%d')}")
            
            today = datetime.now().date()
            next_birthday = person_info['birthday'].replace(year=today.year if today <= person_info['birthday'] else today.year + 1)
            days_until_next_birthday = (next_birthday - today).days
            st.write(f"Days until next birthday: {days_until_next_birthday} days")

            days_in_advance = st.number_input("Days in advance to plan the party", min_value=0, value=30)
            initial_plan_date = next_birthday - timedelta(days=days_in_advance)
            adjusted_date, message = adjust_to_nearest_saturday(initial_plan_date)
            st.write(message)
            st.write(f"Planning date: {adjusted_date.strftime('%A, %Y-%m-%d')}")

    if st.button("Show All Plans"):
        st.subheader("All Birthday Plans:")
        for person_name, details in st.session_state.people.items():
            st.write(f"{person_name} ({details['relationship']}): Birthday on {details['birthday'].strftime('%Y-%m-%d')}")

main()
