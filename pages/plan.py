import streamlit as st

def adjust_plan_date(plan_date):
    # Adjust to the nearest Saturday
    if plan_date.weekday() in [0, 1]: # Monday, Tuesday
        return plan_date - timedelta(days=(plan_date.weekday() + 2))
    elif plan_date.weekday() in [2, 3, 4]: # Wednesday, Thursday, Friday
        return plan_date + timedelta(days=(5 - plan_date.weekday()))
    return plan_date

days = st.number_input('How long would you like to prepare for your birthday party',min_value=0,value=7,step=1)
plan_date = adjust_plan_date(birthday.replace(year=today.year)-timedelta(days=days_before))
st.write('Your plainning date is:',plan_date)

