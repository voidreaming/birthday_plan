import streamlit as st
from datetime import datetime, timedelta

# Ensure 'people', 'current_index', and 'planning_done' are initialized
if 'people' not in st.session_state:
    st.session_state.people = {}
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'data_done' not in st.session_state:
    st.session_state.data_done = False
if 'planning_done' not in st.session_state:
    # planing_date = datetime.now().date()
    st.session_state.planning_done = False


def is_within_holiday_period(plan_date):
    if (plan_date.month == 5 and 1 <= plan_date.day <= 3) or (plan_date.month == 10 and 1 <= plan_date.day <= 7):
        return True
    return False

def adjust_to_nearest_saturday(plan_date):
    # If the date is within the holiday period, no adjustment is needed
    if is_within_holiday_period(plan_date):
        adjustment_message = "It's a holiday period, so no adjustment is made."
        return plan_date, adjustment_message
    
    # Adjust to the nearest Saturday if not within the holiday period
    if plan_date.weekday() in [0, 1]:  # Monday or Tuesday
        adjusted_date = plan_date - timedelta(days=plan_date.weekday() + 1)
        adjustment_message = "It's a weekday, so we've adjusted to the previous Saturday."
    elif 2 <= plan_date.weekday() <= 4:  # Wednesday to Friday
        adjusted_date = plan_date + timedelta(days=5 - plan_date.weekday())
        adjustment_message = "It's a weekday, so we've adjusted to the next Saturday."
    else:
        adjusted_date = plan_date
        adjustment_message = "It's already a weekend, no adjustment needed."
    return adjusted_date, adjustment_message

def calculate_days_until_next_birthday(birthday):
    """Calculate days until the next birthday."""
    today = datetime.now().date()
    next_birthday = birthday.replace(year=today.year if today <= birthday else today.year + 1)
    return (next_birthday - today).days, next_birthday

# def adjust_to_nearest_saturday(plan_date):
#     """Adjust to the nearest Saturday, unless within specified holiday periods."""
#     if (plan_date.month == 5 and 1 <= plan_date.day <= 3) or (plan_date.month == 10 and 1 <= plan_date.day <= 7):
#         return plan_date, "It's a holiday period, so no adjustment is made."
#     # Adjustment logic as previously defined

# Step 1: Data Entry
def data_entry():
    with st.form("person_form"):
        st.subheader("Enter Friend or Family Member's Details")
        name = st.text_input("Name").strip()
        relationship = st.selectbox("Relationship", ["Father", "Mother", "Grandfather", "Grandmother", "Girlfriend", "Classmate", "Friend", "Other"])
        birthday = st.date_input("Date of Birth")
        submit_button = st.form_submit_button("Save")
    if submit_button:
        print("enter if")
        st.session_state.people[name] = {"relationship": relationship, "birthday": birthday}
        st.success(f"Saved {name}'s information!")
        st.session_state.data_done = True

# Step 2 & 3: Planning Process and Confirmation
def plan_birthday():
    if st.session_state.current_index < len(st.session_state.people):
        person_name = list(st.session_state.people)[st.session_state.current_index]
        person_info = st.session_state.people[person_name]
        days_until_next_birthday, next_birthday = calculate_days_until_next_birthday(person_info["birthday"])
        
        st.subheader(f"Planning Birthday for {person_name}")
        st.write(f"Relationship: {person_info['relationship']}")
        st.write(f"Next Birthday: {next_birthday} (in {days_until_next_birthday} days)")
        
        days_in_advance = st.number_input("How many days in advance to plan?", min_value=0, value=30, key="advance_days")
        initial_plan_date = next_birthday - timedelta(days=days_in_advance)
        adjusted_plan_date, message = adjust_to_nearest_saturday(initial_plan_date)
        st.write(f"📅 Your initially planned date is:", initial_plan_date.strftime('%A, %Y-%m-%d'))   
        st.write(f"🔧 {message}")
        st.write(f"📅 Your adjusted planning date is:",  adjusted_plan_date.strftime('%A, %Y-%m-%d'))
        
        if st.button("Confirm Planning Date"):
            st.session_state.people[person_name]["planning_date"] = adjusted_plan_date
            st.session_state.current_index += 1
            
            if st.session_state.current_index >= len(st.session_state.people):
                st.session_state.planning_done = True
                st.success("All birthday plans confirmed!")
    else:
        st.session_state.planning_done = True

# Step 4: Summary and Review
def show_summary():
    st.subheader("Summary of All Birthday Plans")
    for name, info in st.session_state.people.items():
        birthday = info['birthday'].strftime('%Y-%m-%d')  # Format birthday here
        planning_date = info.get("planning_date")
        if planning_date:
            planning_date = planning_date.strftime('%Y-%m-%d')
        else:
            planning_date = "Not set"
        st.write(f"{name} ({info['relationship']}): Birthday on {birthday}, Planning Date: {planning_date}")
    if st.button("Plan Another Birthday"):
        # Reset for another round of planning
        st.session_state.current_index = 0
        st.session_state.planning_done = False


# def main():
#     st.title("🎉 Birthday Party Planner")
    
#     if not st.session_state.planning_done:
#         data_entry()
#         print("first satge done")
#         plan_birthday()
#     else:
#         show_summary()
def main():
    data_entry()
    if st.session_state.data_done:
        plan_birthday()
    if st.session_state.planning_done:
        show_summary()

main()
