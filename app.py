import streamlit as st
from datetime import datetime, timedelta

import streamlit as st

# Custom CSS to style the markdown
st.markdown("""
<style>
.big-font {
    font-size:24px !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state variables for stage control and user inputs
if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'birthday' not in st.session_state:
    st.session_state.birthday = datetime.now().date()

#contributed by 李澍
def calculate_days_until_next_birthday(birthday, today):
    next_year = today.year + (today >= birthday.replace(year=today.year))
    next_birthday = birthday.replace(year=next_year)
    return (next_birthday - today).days
#contributed by 李澍
def adjust_to_nearest_saturday(plan_date):
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

#contributed by 汪守菊
def main():
    today = datetime.now().date()
    st.title("🎉 Birthday Party Planner")
    # for _ in range(2):  # Adjust the range to increase or decrease the space
    #     st.write("")

    col1, col2, col3 = st.columns([1,2,1]) 


    if st.session_state.stage == 0:
        st.write("## Welcome to Birthday Party Plan! 👋")
        st.markdown(
            """
            This interactive tool is designed to simplify your birthday planning process. 
            Whether you're organizing a small gathering or a grand celebration, we're here to help you every step of the way.

            Here's what you can do:
            * **Calculate the days** until your next birthday.
            * **Plan ahead** by selecting the best date to prepare for your party, with recommendations for the weekend.
            * **Visualize** your planning timeline with ease.

            Let's make your next birthday celebration unforgettable. Click Start Planning below to begin the journey!
            """ )
        # with col2:
        #     if st.button('🚀 Start Planning'):
        #         st.session_state.stage = 1
        if st.button('🚀 Start Planning'):
            st.session_state.stage = 1

    elif st.session_state.stage == 1:  # Changed to elif
        st.session_state.birthday = st.date_input("🎂 Enter your birthday :", min_value=datetime(today.year - 100, 1, 1), max_value=datetime(today.year + 1, 12, 31), value=datetime(today.year, today.month, today.day))
        days_until_birthday = calculate_days_until_next_birthday(st.session_state.birthday, today)
        st.write(f"Days until your next birthday:", days_until_birthday)
        if st.button('🔜 Proceed to Planning '):
            st.session_state.stage = 2

    elif st.session_state.stage == 2:  # Changed to elif
        # days_until_birthday = calculate_days_until_next_birthday(st.session_state.birthday, today)
        # st.write(f"Days until your next birthday:", days_until_birthday)
        # days_in_advance = st.number_input("Enter how many days in advance you want to plan the party ⏳:", min_value=1, value=30, step=1)
        # planned_day = st.session_state.birthday.replace(year=today.year if today <= st.session_state.birthday else today.year + 1) - timedelta(days=days_in_advance)
        # planned_date, adjustment_message= adjust_to_nearest_saturday(planned_day)
        #  #add message
        # st.write(f"📅 Your initially planned date is: {planned_day.strftime('%A, %Y-%m-%d')}")
        # st.write(f"🔧 {adjustment_message}")
        # st.write(f"📅 Your adjusted planning date is: {planned_date.strftime('%A, %Y-%m-%d')}")
        # if st.button('Confirm Plan Date ✅'):
        #     st.session_state.planned_date = planned_date
        #     st.session_state.stage = 3
        days_in_advance = st.number_input("⏳ Enter how many days in advance you want to plan the party:", min_value=0, value=30)
        planned_day = st.session_state['birthday'].replace(year=today.year if today <= st.session_state['birthday'] else today.year + 1) - timedelta(days=days_in_advance)
        planned_date, adjustment_message = adjust_to_nearest_saturday(planned_day)
        st.write(f"📅 Your initially planned date is:", planned_day.strftime('%A, %Y-%m-%d'))   
        # st.write(f"📅 Your initially planned date is:", planned_day)
        st.write(f"🔧 {adjustment_message}")
        st.write(f"📅 Your adjusted planning date is:",  planned_date.strftime('%A, %Y-%m-%d'))
        if st.button('✅ Confirm and Show Results'):
            st.session_state['planned_date'] = planned_date
            st.session_state['stage'] = 3

    elif st.session_state.stage == 3:  # Changed to elif
        st.write(f"🎉 Your previous party planning date is set for:", st.session_state['planned_date'])
        st.write('❓Do you want to choose preparation date again or finish?')

        if st.button('🔄 Reset Plan Date'):
            st.session_state['stage'] = 2
        elif st.button('🏁 Finish'):
            st.session_state['stage'] = 4

    elif st.session_state.stage == 4:  # Added elif for exclusive stage 4 content
        st.markdown(
            """
            ### 🌟 Congratulations on completing your birthday party plan!
            
            Your party is now on track to be a memorable event, thanks to your thoughtful planning and organization. 

            What's Next?

            * **Invite Your Guests:** It's time to let them know about the upcoming celebration.
            * **Finalize Details:** From the venue to the menu, ensure every aspect of your party is as perfect as you've imagined.
            * **Enjoy Your Party:** Remember, the goal is to celebrate and create lasting memories. Have fun!

            """ )
        st.write("👋 Thank you for using the Birthday Party Planner!")

main()

