import os
import pandas as pd
import streamlit as st

# Define the path to the cleaned CSV file
csv_path = '/Users/mattgoldfeder/Downloads/cleaned_workoutdb2.csv'

# Load the cleaned CSV file into a DataFrame
try:
    df = pd.read_csv(csv_path, header=0)
    st.success(f'Successfully loaded the exercise database.')
except Exception as e:
    st.error(f'Error loading CSV file: {e}')
    st.stop()

# Streamlit UI Elements
st.title('Workout Generator')

# Ask if the workout focus is on size or strength
workout_focus = st.radio('What is your workout goal?', ['Size (Hypertrophy)', 'Strength'])

# Multi-select for target muscle groups
all_muscle_groups = df['target_muscle_group'].dropna().unique().tolist()
body_parts = st.multiselect('Select target muscle groups', all_muscle_groups)

# Allow user to select the number of exercises per muscle group
muscle_group_counts = {}
for muscle in body_parts:
    muscle_group_counts[muscle] = st.slider(f'Number of exercises for {muscle}', min_value=0, max_value=10, value=1)

# Generate workout button
if st.button('Generate Workout'):
    try:
        selected_exercises = pd.DataFrame()

        # Collect exercises for each muscle group based on user input
        for muscle, count in muscle_group_counts.items():
            if count > 0:
                muscle_exercises = df[(df['primary_exercise_classification'].str.lower() == 'bodybuilding') &
                                      (df['primary_equipment'].str.lower().isin(['bodyweight', 'dumbbell', 'cable', 'barbell', 'pull up bar'])) &
                                      (df['target_muscle_group'].str.lower() == muscle.lower())]
                selected_exercises = pd.concat([selected_exercises, muscle_exercises.head(count)])

        # Display the selected exercises if available
        if not selected_exercises.empty:
            st.success(f'Found {len(selected_exercises)} exercise(s) for the selected muscle groups:')
            st.dataframe(selected_exercises[['exercise', 'target_muscle_group', 'primary_equipment']])

            # Provide workout guidelines based on the focus
            if workout_focus == 'Strength':
                st.subheader('Strength Workout Guidelines')
                st.markdown('''
                **Goal:** Increase the amount of weight you can lift, focusing on the nervous system and muscle recruitment.
                - **Reps:** 1-6 reps per set
                - **Sets:** 3-6 sets per exercise
                - **Weight:** 85-100% of your 1-rep max (1RM)
                - **Rest:** 2-5 minutes between sets
                - **Tempo:** Explosive on the lift, controlled lowering
                - **Exercises:** Compound movements (e.g., squats, deadlifts, bench press, pull-ups)
                - **Frequency:** 2-3 times per week per muscle group, allowing recovery
                - **Progression:** Emphasis on progressively lifting heavier weights over time
                - **Training Style:** Lower volume, higher intensity
                ''')
            else:
                st.subheader('Size/Hypertrophy Workout Guidelines')
                st.markdown('''
                **Goal:** Increase muscle size through hypertrophy by causing microtears in muscle fibers that repair bigger and stronger.
                - **Reps:** 6-12 reps per set
                - **Sets:** 3-5 sets per exercise
                - **Weight:** 65-85% of your 1RM
                - **Rest:** 30-90 seconds between sets
                - **Tempo:** Moderate (e.g., 2-3 seconds lowering, 1 second lifting)
                - **Exercises:** Mix of compound and isolation movements
                - **Frequency:** Higher frequency, 3-6 days per week with split routines
                - **Progression:** Focus on volume and progressive overload
                - **Training Style:** Higher volume, moderate intensity, focus on muscle "pump" and time under tension
                ''')
        else:
            st.warning('No exercises found matching the criteria. Try adjusting the muscle groups or exercise counts.')
    except KeyError as e:
        st.error(f'Column not found: {e}')
