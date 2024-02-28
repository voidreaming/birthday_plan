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
 
# Set the app title 
st.title('Birthday Party Planer') 
# Add a welcome message 
st.write('Choose Your Birthday!') 
# Create a date input 
birthday = st.date_input("what is your birthday?",value=datetime.now())
#calculate the days before the next birthday
today = datetime.now().date()
days_to_birthday = calculate_days_to_next_birthday(birthday,today)
st.write('Days left for the next birthday:',days_to_birthday)

st.write('Now press any keys you like to enter the plan making stage')

# Display the customized message 
#st.write('Customized Message:', user_input)
