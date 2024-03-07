import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

if 'data_done' not in st.session_state:
    st.session_state.data_done = False
if 'planning_done' not in st.session_state:
    st.session_state.planning_done = False
if 'end_done' not in st.session_state:
    st.session_state.end_done = False


# Part 1: Define a function to input and save information about family members and friends
def input_family_and_friends():
    st.markdown("## 📝 Family Members and Friends Information")
    num_people = st.number_input(
        "👥 Enter the number of family members and friends:",
        min_value=0,
        step=1,
        value=0)
    today = datetime.now().date()
    people_info = []

    if num_people > 0:
        st.markdown("----")  # Add a divider for visual separation

    for i in range(num_people):
        with st.container(
        ):  # Use a container for each person's inputs to group them visually
            st.markdown(f"### Person {i+1}")
            cols = st.columns([3, 2, 3])  # Adjust column ratios as needed
            name = cols[0].text_input("👤 Name:", key=f"name_{i}")
            relationship = cols[1].selectbox("🤝 Relationship:", [
                "Father", "Mother", "Grandfather", "Grandmother", "Spouse",
                "Partner", "Sibling", "Friend", "Other"
            ],
                                             key=f"relationship_{i}")
            birthday = cols[2].date_input(
                "🎂 Birthday:",
                min_value=datetime(today.year - 100, 1, 1),
                max_value=datetime(today.year + 1, 12, 31),
                value=datetime(today.year, today.month, today.day),
                key=f"birthday_{i}")
            people_info.append({
                "Name": name,
                "Relationship": relationship,
                "Birth Date": birthday
            })
            st.markdown(
                "---"
            )  # Add a subtle divider between inputs for different people

    if st.button("💾 Save"):
        df = pd.DataFrame(people_info)
        st.session_state['df_people'] = df
        st.success("📥 Information Saved Successfully!")
        st.dataframe(df)  # Display the dataframe in a more compact way


def is_within_holiday_period(plan_date):
    if (plan_date.month == 5
            and 1 <= plan_date.day <= 3) or (plan_date.month == 10
                                             and 1 <= plan_date.day <= 7):
        return True
    return False


def adjust_to_nearest_saturday(plan_date):
    if is_within_holiday_period(plan_date):
        return plan_date, "It's a holiday period, so no adjustment is made."
    if plan_date.weekday() in [0, 1]:  # Monday or Tuesday
        adjusted_date = plan_date - timedelta(days=plan_date.weekday() + 2)
        adjustment_message = "Adjusted to the previous Saturday."
    elif 2 <= plan_date.weekday() <= 4:  # Wednesday to Friday
        adjusted_date = plan_date + timedelta(days=5 - plan_date.weekday())
        adjustment_message = "Adjusted to the next Saturday."
    else:
        adjusted_date = plan_date
        adjustment_message = "No adjustment needed, it's already a weekend."
    return adjusted_date, adjustment_message


def calculate_days_until_next_birthday(birthday):
    today = datetime.now().date()
    this_year_birthday = birthday.replace(year=today.year)
    next_birthday = this_year_birthday if this_year_birthday > today else this_year_birthday.replace(
        year=this_year_birthday.year + 1)
    return (next_birthday - today).days, next_birthday


# Part 2: Planning part
def planning_part(df_people):
    st.markdown("## 🎉 Birthday Party Planning")
    selected_person = st.selectbox("👤 Select a person:", df_people["Name"])

    person_info = df_people[df_people["Name"] == selected_person].iloc[0]
    birthday = person_info["Birth Date"]

    idx = df_people.index[df_people['Name'] == selected_person].tolist()[0]
    st.markdown(f"### 📅 Birthday Information for {selected_person}")
    days_until_birthday, next_birthday = calculate_days_until_next_birthday(
        birthday)
    st.write(f"🗓 Days until next birthday: {days_until_birthday}")
    days_in_advance = st.number_input(
        "🕒 Enter number of days in advance to make plans:",
        min_value=0,
        step=1,
        value=0)

    plan_date = next_birthday - timedelta(days=days_in_advance)
    plan_date, adjustment_message = adjust_to_nearest_saturday(plan_date)
    df_people.at[idx, 'Plan Date'] = plan_date
    st.session_state['df_people'] = df_people

    st.markdown(f"### ✅ Plan Date: {plan_date.strftime('%B %d, %Y')}")
    st.info(adjustment_message)


def end_page(df_people):
    st.markdown("## 📋 Birthday Planning Summary")
    for index, row in df_people.iterrows():
        with st.container():
            st.markdown(f"### {row['Name']}")
            cols = st.columns(2)
            cols[0].markdown(f"**Relationship:** {row['Relationship']}")
            cols[0].markdown(
                f"**Birth Date:** {row['Birth Date'].strftime('%B %d, %Y')}")

            if 'Plan Date' in row and not pd.isnull(row['Plan Date']):
                days_until_next_birthday, _ = calculate_days_until_next_birthday(
                    row['Birth Date'])
                cols[1].markdown(
                    f"**Days until next birthday:** {days_until_next_birthday}"
                )
                cols[1].markdown(
                    f"**Planned celebration date:** {row['Plan Date'].strftime('%B %d, %Y')}"
                )
            else:
                cols[1].markdown("**Birthday plan:** Not set")
            st.markdown("---")  # Divider for readability

    redo_planning = st.button("🔄 Plan or Replan Birthdays")
    if redo_planning:
        st.session_state.data_done = False


def goodbye():
    st.markdown("""
    ### 🎊 Congratulations on completing your birthday party plan!
    
    Your party is now on track to be a memorable event, thanks to your thoughtful planning and organization. 

    **What's Next?**
    - **Invite Your Guests:** It's time to let them know about the upcoming celebration.
    - **Finalize Details:** From the venue to the menu, ensure every aspect of your party is as perfect as you've imagined.
    - **Enjoy Your Party:** Remember, the goal is to celebrate and create lasting memories. Have fun!

    **👋 Thank you for using the Birthday Party Planner!**
    """)


def main():
    st.title("🎂 Birthday Party Planner")
    if 'df_people' not in st.session_state:
        st.session_state['df_people'] = pd.DataFrame(
        )  # Initialize in session state if not present
    df_people = input_family_and_friends()

    if st.button("➡️ Continue to make plan"):
        st.session_state.data_done = True

    if st.session_state.data_done and not st.session_state['df_people'].empty:
        planning_part(st.session_state['df_people'])

    if st.button("🔚 End Planning"):
        st.session_state.planning_done = True
        end_page(st.session_state['df_people'])  # Pass the updated dataframe

    finish = st.button("✅ Finish and Exit")
    if finish:
        goodbye()


if __name__ == "__main__":
    main()
