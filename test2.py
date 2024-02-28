import streamlit as st
from datetime import datetime, timedelta

# Initialize session state variables if they don't already exist
if 'stage' not in st.session_state:
    st.session_state['stage'] = 0  # Control flow of the application stages
if 'birthday' not in st.session_state:
    st.session_state['birthday'] = datetime.now().date()  # Default value

# Function to calculate days until the next birthday
def calculate_days_until_next_birthday(birthday, today):
    next_year = today.year + (today >= birthday.replace(year=today.year))
    next_birthday = birthday.replace(year=next_year)
    return (next_birthday - today).days

# Function to adjust the planning date to the nearest Saturday
def adjust_to_nearest_saturday(plan_date):
    if plan_date.weekday() in [0, 1]:  # Monday or Tuesday
        return plan_date - timedelta(days=plan_date.weekday() + 1)
    elif 2 <= plan_date.weekday() <= 4:  # Wednesday to Friday
        return plan_date + timedelta(days=5 - plan_date.weekday())
    return plan_date

def main():
    st.title("🎉 Welcome to the Birthday Party Planner!")

    # Define 'today' at the beginning of the function to ensure it's available when needed
    today = datetime.now().date()

    # Stage 0: Welcome screen
    if st.session_state['stage'] == 0:
        if st.button('🚀 Click here to start'):
            st.session_state['stage'] = 1
    
    # Stage 1: Enter birthday and today's date
    if st.session_state['stage'] == 1:
        st.session_state['birthday'] = st.date_input("🎂 Enter your birthday:", value=datetime.now())
        days_until_birthday = calculate_days_until_next_birthday(st.session_state['birthday'], today)
        st.write("📆 Days until your next birthday:", days_until_birthday)
        if st.button('🎈 Plan Your Birthday Party'):
            st.session_state['stage'] = 2
            st.session_state['days_until_birthday'] = days_until_birthday
    
    # Stage 2: Planning the birthday party
    if st.session_state['stage'] == 2:
        if 'days_until_birthday' in st.session_state:
            days_in_advance = st.number_input("Enter how many days in advance you want to plan the party:", min_value=0, value=30)
            planned_date = adjust_to_nearest_saturday(st.session_state['birthday'].replace(year=today.year if today <= st.session_state['birthday'] else today.year + 1) - timedelta(days=days_in_advance))
            st.write(f"📅 Your planned date is:", planned_date)
            if st.button('✅ Confirm and Show Results'):
                st.session_state['planned_date'] = planned_date
                st.session_state['stage'] = 3
    
    # Stage 3: Display results and offer to reset or finish
    if st.session_state['stage'] == 3:
        st.write(f"🎉 Your party planning date is set for:", st.session_state['planned_date'])
        if st.button('🔄 Reset Plan Date'):
            st.session_state['stage'] = 2  # Go back to planning stage
        elif st.button('🏁 Finish'):
            st.write("👋 Thank you for using the Birthday Party Planner!")
            st.session_state['stage'] = 4  # Conclude

main()

