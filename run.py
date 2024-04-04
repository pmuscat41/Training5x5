import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(layout="wide")

# Helper function to save workout data to CSV
def save_data(data):
    data.to_csv('workout_data.csv', index=False)

# Helper function to load workout data from CSV
def load_data():
    try:
        data = pd.read_csv('workout_data.csv')
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Date', 'Exercise', 'Set', 'Weight', 'Reps', 'Time', 'Distance'])
    return data

# Helper function to get the last recorded weight for an exercise
def get_last_weight(data, exercise):
    last_weight = data[data['Exercise'] == exercise]['Weight'].iloc[-1] if not data[data['Exercise'] == exercise].empty else 0
    return int(last_weight)

# Main app
def main():
    st.title('Gym Workout Tracker')

    # Load workout data
    workout_data = load_data()

    # Sidebar
    st.sidebar.title('Timer')
    timer_duration = st.sidebar.selectbox('Timer Duration', ['30 seconds', '1 minute', '1.5 minutes', '2 minutes'])

    # Timer
    if st.sidebar.button('Start Timer'):
        timer_seconds = int(timer_duration.split(' ')[0]) if 'seconds' in timer_duration else int(timer_duration.split(' ')[0]) * 60
        timer_placeholder = st.sidebar.empty()
        while timer_seconds > 0:
            minutes, seconds = divmod(timer_seconds, 60)
            timer_text = f"{minutes:02d}:{seconds:02d}"
            timer_placeholder.header(timer_text)
            time.sleep(1)
            timer_seconds -= 1
        timer_placeholder.header("Time's up!")
        st.sidebar.success("Workout complete!")

    # Reporting
    st.sidebar.header('Workout Report')
    if not workout_data.empty:
        min_date = pd.to_datetime(workout_data['Date']).min().date()
        max_date = pd.to_datetime(workout_data['Date']).max().date()
        date_range = st.sidebar.date_input('Select Date Range', [min_date, max_date], min_value=min_date, max_value=max_date)
        filtered_data = workout_data[(workout_data['Date'] >= date_range[0].strftime('%Y-%m-%d')) & (workout_data['Date'] <= date_range[1].strftime('%Y-%m-%d'))]
        if not filtered_data.empty:
            st.sidebar.dataframe(filtered_data)
            if st.sidebar.button('Export to CSV'):
                filtered_data.to_csv('workout_report.csv', index=False)
                st.sidebar.success('Workout report exported to CSV!')
        else:
            st.sidebar.info('No workout data available for the selected date range.')
    else:
        st.sidebar.info('No workout data available.')

    # Tabs for different exercises
    tab_push, tab_pull, tab_skipping, tab_treadmill, tab_spinning = st.tabs(['Push Day', 'Pull Day', 'Skipping', 'Treadmill', 'Spinning'])

    with tab_push:
        st.header('Push Day')
        exercises = ['Dumbbell Squats', 'Incline Dumbbell Press', 'Dumbbell Shoulder Press', 'Shoulder Supersets']
        for exercise in exercises:
            st.subheader(exercise)
            last_weight = get_last_weight(workout_data, exercise)
            col1, col2, col3, col4, col5 = st.columns(5)
            weights = []
            reps = []
            for i, col in enumerate([col1, col2, col3, col4, col5]):
                with col:
                    st.write(f'Set {i+1}')
                    weight = st.number_input(f'Weight (kg)', min_value=0, value=last_weight, step=1, key=f'{exercise}_weight_set{i+1}')
                    rep = st.number_input(f'Reps', min_value=0, step=1, key=f'{exercise}_reps_set{i+1}')
                    weights.append(weight)
                    reps.append(rep)
            if st.button(f'Save {exercise}'):
                new_data = pd.DataFrame({'Date': [datetime.now().strftime("%Y-%m-%d")] * 5,
                                         'Exercise': [exercise] * 5,
                                         'Set': list(range(1, 6)),
                                         'Weight': weights,
                                         'Reps': reps,
                                         'Time': [''] * 5,
                                         'Distance': [''] * 5})
                workout_data = pd.concat([workout_data, new_data], ignore_index=True)
                save_data(workout_data)
                st.success(f'{exercise} data saved!')

    with tab_pull:
        st.header('Pull Day')
        exercises = ['Deadlifts', 'Bent Over Rows', 'Bicep Curls']
        for exercise in exercises:
            st.subheader(exercise)
            last_weight = get_last_weight(workout_data, exercise)
            col1, col2, col3, col4, col5 = st.columns(5)
            weights = []
            reps = []
            for i, col in enumerate([col1, col2, col3, col4, col5]):
                with col:
                    st.write(f'Set {i+1}')
                    weight = st.number_input(f'Weight (kg)', min_value=0, value=last_weight, step=1, key=f'{exercise}_weight_set{i+1}')
                    rep = st.number_input(f'Reps', min_value=0, step=1, key=f'{exercise}_reps_set{i+1}')
                    weights.append(weight)
                    reps.append(rep)
            if st.button(f'Save {exercise}'):
                new_data = pd.DataFrame({'Date': [datetime.now().strftime("%Y-%m-%d")] * 5,
                                         'Exercise': [exercise] * 5,
                                         'Set': list(range(1, 6)),
                                         'Weight': weights,
                                         'Reps': reps,
                                         'Time': [''] * 5,
                                         'Distance': [''] * 5})
                workout_data = pd.concat([workout_data, new_data], ignore_index=True)
                save_data(workout_data)
                st.success(f'{exercise} data saved!')

    with tab_skipping:
        st.header('Skipping')
        col1, col2, col3, col4, col5 = st.columns(5)
        reps = []
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.write(f'Set {i+1}')
                rep = st.number_input(f'Skipping Reps', min_value=0, step=10, key=f'skipping_reps_set{i+1}')
                reps.append(rep)
        if st.button('Save Skipping'):
            new_data = pd.DataFrame({'Date': [datetime.now().strftime("%Y-%m-%d")] * 5,
                                     'Exercise': ['Skipping'] * 5,
                                     'Set': list(range(1, 6)),
                                     'Weight': [''] * 5,
                                     'Reps': reps,
                                     'Time': [''] * 5,
                                     'Distance': [''] * 5})
            workout_data = pd.concat([workout_data, new_data], ignore_index=True)
            save_data(workout_data)
            st.success('Skipping data saved!')

    with tab_treadmill:
        st.header('Treadmill')
        col1, col2, col3, col4, col5 = st.columns(5)
        times = []
        distances = []
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.write(f'Set {i+1}')
                time_mins = st.number_input(f'Treadmill Time (minutes)', min_value=0, step=1, key=f'treadmill_time_set{i+1}')
                distance_km = st.number_input(f'Treadmill Distance (km)', min_value=0.0, step=0.1, key=f'treadmill_distance_set{i+1}')
                times.append(time_mins)
                distances.append(distance_km)
        if st.button('Save Treadmill'):
            new_data = pd.DataFrame({'Date': [datetime.now().strftime("%Y-%m-%d")] * 5,
                                     'Exercise': ['Treadmill'] * 5,
                                     'Set': list(range(1, 6)),
                                     'Weight': [''] * 5,
                                     'Reps': [''] * 5,
                                     'Time': times,
                                     'Distance': distances})
            workout_data = pd.concat([workout_data, new_data], ignore_index=True)
            save_data(workout_data)
            st.success('Treadmill data saved!')

    with tab_spinning:
        st.header('Spinning')
        col1, col2, col3, col4, col5 = st.columns(5)
        times = []
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.write(f'Set {i+1}')
                time_mins = st.number_input(f'Spinning Time (minutes)', min_value=0, step=1, key=f'spinning_time_set{i+1}')
                times.append(time_mins)
        if st.button('Save Spinning'):
            new_data = pd.DataFrame({'Date': [datetime.now().strftime("%Y-%m-%d")] * 5,
                                     'Exercise': ['Spinning'] * 5,
                                     'Set': list(range(1, 6)),
                                     'Weight': [''] * 5,
                                     'Reps': [''] * 5,
                                     'Time': times,
                                     'Distance': [''] * 5})
            workout_data = pd.concat([workout_data, new_data], ignore_index=True)
            save_data(workout_data)
            st.success('Spinning data saved!')

if __name__ == '__main__':
    main()