import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
teachers = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Teachers")
courses = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Courses")
transactions = pd.read_excel("EduPro Online Platform.xlsx", sheet_name="Transactions")

# Merge datasets
merged = transactions.merge(teachers, on="TeacherID").merge(courses, on="CourseID")

st.title("EduPro Course Quality Evaluation Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
expertise = st.sidebar.selectbox("Select Expertise", merged['Expertise'].unique())
category = st.sidebar.selectbox("Select Course Category", merged['CourseCategory'].unique())

filtered = merged[(merged['Expertise'] == expertise) & (merged['CourseCategory'] == category)]

st.subheader("Instructor Performance Leaderboard")
leaderboard = filtered.groupby('TeacherName')['TeacherRating'].mean().sort_values(ascending=False)
st.bar_chart(leaderboard)

st.subheader("Experience vs Teacher Rating")
st.scatter_chart(filtered[['YearsOfExperience', 'TeacherRating']])

st.subheader("Course Quality by Category and Level")

pivot = merged.pivot_table(values='CourseRating', index='CourseCategory', columns='CourseLevel', aggfunc='mean')

fig, ax = plt.subplots()
sns.heatmap(pivot, annot=True, cmap="Blues", ax=ax)
st.pyplot(fig)

st.subheader("Key Performance Indicators")

avg_teacher_rating = merged['TeacherRating'].mean()
avg_course_rating = merged['CourseRating'].mean()
rating_consistency = merged['TeacherRating'].std()

st.metric("Average Teacher Rating", f"{avg_teacher_rating:.2f}")
st.metric("Average Course Rating", f"{avg_course_rating:.2f}")
st.metric("Rating Consistency Index", f"{rating_consistency:.2f}")
