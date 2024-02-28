import streamlit as st
from datetime import datetime, timedelta

def calculate_days_to_next_birthday(birthday, today):
    next_birthday = birthday.replace(year=today.year)
    if today > next_birthday:
        next_birthday = next_birthday.replace(year=today.year + 1)
    return (next_birthday - today).days

def adjust_plan_date(plan_date):
    # Adjust to the nearest Saturday
    if plan_date.weekday() in [0, 1]: # Monday, Tuesday
        return plan_date - timedelta(days=(plan_date.weekday() + 2))
    elif plan_date.weekday() in [2, 3, 4]: # Wednesday, Thursday, Friday
        return plan_date + timedelta(days=(5 - plan_date.weekday()))
    return plan_date

def app_flow():
    st.title("Birthday Party Planner")
    
    # Step 1: Welcome and proceed
    if st.button('Click here to start planning'):
        # Step 2: Input for birth date and today's date
        birthday = st.date_input("What's your birth date?", value=datetime.now())
        today = datetime.now().date()
        days_to_birthday = calculate_days_to_next_birthday(birthday, today)
        st.write(f"Days until your next birthday: {days_to_birthday}")
    print("sucess")
        
    if st.button('Plan Your Party'):
          # Step 3: Planning logic
        days_before = st.number_input('How many days before your birthday do you want to start planning?', min_value=0, value=30, step=1)
        plan_date = adjust_plan_date(birthday.replace(year=today.year) - timedelta(days=days_before))
        st.write(f"Your planning date is: {plan_date}")
            
            # Step 4: Review and confirm the plan
    if st.button('Confirm and Proceed'):
        st.write(f"Planning Date: {plan_date.strftime('%A, %d %B %Y')}")
                # Option to re-plan or finalize
        redo_plan = st.button('Adjust Planning Date')
        if redo_plan:
            st.experimental_rerun()
        else:
            st.success("Your planning date has been set. Happy planning!")
                    
# Run the app flow
app_flow()

