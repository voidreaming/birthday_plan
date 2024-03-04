import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

if 'data_done' not in st.session_state:
    st.session_state.data_done = False
if 'planning_done' not in st.session_state:
    # planing_date = datetime.now().date()
    st.session_state.planning_done = False

# Part1 : Define a function to input and save information about family members and friends
def input_family_and_friends():
    st.header("Family Members and Friends Information")
    num_people = st.number_input("Enter the number of family members and friends:", min_value=0, step=1, value=0)
    today = datetime.now().date()
    people_info = []
    df = pd.DataFrame(people_info)
    for i in range(num_people):
        st.subheader(f"Person {i+1}")
        name = st.text_input(f"Enter name for person {i+1}:")
        relationship = st.selectbox(f"Select relationship for person {i+1}:", ["Father", "Mother", "Grandfather", "Grandmother", "Girlfriend", "Boyfriend", "Classmate", "Friend", "Other"])
        birthday = st.date_input(f"🎂 Enter birthday for person {i+1}:", min_value=datetime(today.year - 100, 1, 1), max_value=datetime(today.year + 1, 12, 31), value=datetime(today.year, today.month, today.day), key=f"birthday_{i}")

        people_info.append({"Name": name, "Relationship": relationship, "Birth Date": birthday})

    if st.button("Save"):
        df = pd.DataFrame(people_info)
        st.session_state['df_people'] = df 
        st.write(df)
    # st.session_state.data_done = True
    return df

#define a function to determine the date
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

#Part2 : Planing part.
def planning_part(df_people):
    st.header("Birthday Party Planning")
    selected_person = st.selectbox("Select a person:", df_people["Name"])

    person_info = df_people[df_people["Name"] == selected_person].iloc[0]
    birthday = person_info["Birth Date"]

    st.subheader("Birthday Information:")
    st.write(f"Next birthday for {selected_person}: {birthday.strftime('%B %d, %Y')}")

    days_until_birthday, next_birthday = calculate_days_until_next_birthday(birthday)
    st.write(f"Number of days until next birthday: {days_until_birthday}")

    days_in_advance = st.number_input("Enter number of days in advance to make plans:", min_value=0, step=1, value=0)

    plan_date = next_birthday - timedelta(days=days_in_advance)
    plan_date, adjustment_message = adjust_to_nearest_saturday(plan_date)

    st.session_state.planning_done = True
    st.subheader("Plan Date:")
    st.write(f"Plan date for {selected_person}: {plan_date.strftime('%B %d, %Y')}")
    st.write(adjustment_message)


# def main():
#     st.title("Birthday Party Planner")

#     # Input family members and friends information
#     df_people = {}
#     df_people = input_family_and_friends()
#     st.write(df_people)
#     # print(f'qqq{df_people.shape}')
#     # if not df_people.empty:
#     #     st.session_state.data_done = True
    
#     if st.button("Countinue to make plan"):
#         st.session_state.data_done = True
#         # print(st.session_state.data_done)   
#     if st.session_state.data_done:
#         planning_part(df_people)
def main():
    st.title("Birthday Party Planner")
    if 'df_people' not in st.session_state:
        st.session_state['df_people'] = pd.DataFrame()  # Initialize in session state if not present
    df_people = input_family_and_friends()

    if st.button("Continue to make plan"):
        st.session_state.data_done = True

    if st.session_state.data_done and not st.session_state['df_people'].empty:
        planning_part(st.session_state['df_people'])
    

if __name__ == "__main__":
    main()
