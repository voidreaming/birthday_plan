import streamlit as st
from datetime import datetime, timedelta

def calculate_days_until_birthday(birthday: datetime.date, today: datetime.date):
    this_year_birthday = birthday.replace(year=today.year)
    today = datetime.today().date()
    if today > this_year_birthday:
        next_year_birthday = this_year_birthday.replace(year=today.year + 1)
        return (next_year_birthday - today).days
    else:
        return (this_year_birthday - today).days

def determine_plan_date(birthday: datetime, plan_days_before: int, today: datetime):
    next_birthday_year = today.year if today <= birthday.replace(year=today.year) else today.year + 1
    next_birthday = birthday.replace(year=next_birthday_year)
    plan_date = next_birthday - timedelta(days=plan_days_before)
    
    if plan_date.weekday() >= 5: # Adjust for Saturday if on weekend
        plan_date -= timedelta(days=(plan_date.weekday() - 4))
    return plan_date

st.title("Birthday Party Planner")

if st.button('Start Planning'):
    birthday_input = st.date_input("Enter your birthday:", value=datetime.today())
    today = datetime.today()
    if birthday_input:
        days_until_birthday = calculate_days_until_birthday(birthday=birthday_input, today=today)
        st.write(f"Days until your next birthday: {days_until_birthday}")
        
        if st.button('Proceed to Planning'):
            planning_days_before = st.number_input("How many days before your birthday do you want to plan the party?", min_value=1, value=30, step=1)
            
            if st.button('Determine Plan Date'):
                plan_date = determine_plan_date(birthday=birthday_input, plan_days_before=planning_days_before, today=today)
                st.write(f"Your planning date should be: {plan_date.strftime('%Y-%m-%d')}")
                
                if st.button('Confirm Plan Date'):
                    st.success(f"Your party planning date is set to {plan_date.strftime('%Y-%m-%d')}. Happy planning!")

