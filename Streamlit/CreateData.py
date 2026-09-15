import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Performance Analyzer",
    layout="wide"
)

st.title("Student Performance Analyzer")
st.write("Upload a CSV file to analyze student marks.")

# -----------------------------
# Upload CSV
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.success("CSV uploaded successfully!")

    # -----------------------------
    # Display Dataset
    # -----------------------------
    st.subheader("Dataset")
    st.dataframe(df, use_container_width=True)

    # First column is assumed to be Student Name
    student_column = df.columns[0]

    # Find numeric subject columns
    subject_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if len(subject_columns) == 0:
        st.error("No numeric subject columns found in the CSV.")
        st.stop()

    # -----------------------------
    # Calculate Student Average
    # -----------------------------
    df["Average"] = df[subject_columns].mean(axis=1)

    # -----------------------------
    # Show Summary
    # -----------------------------
    st.subheader("Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", len(df))
    col2.metric("Total Subjects", len(subject_columns))
    col3.metric("Class Average", f"{df['Average'].mean():.2f}")
    col4.metric("Highest Average", f"{df['Average'].max():.2f}")

    # -----------------------------
    # Select Student
    # -----------------------------
    st.subheader("Student Details")

    selected_student = st.selectbox(
        "Select Student",
        df[student_column].tolist()
    )

    student_data = df[
        df[student_column] == selected_student
    ].iloc[0]

    # -----------------------------
    # Display Individual Marks
    # -----------------------------
    st.write(f"### {selected_student}")

    marks = {}

    for subject in subject_columns:
        marks[subject] = student_data[subject]

    marks_df = pd.DataFrame(
        list(marks.items()),
        columns=["Subject", "Marks"]
    )

    st.dataframe(
        marks_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # PASS / FAIL
    # -----------------------------
    # Passing mark = 40
    passing_marks = 40

    failed_subjects = [
        subject
        for subject in subject_columns
        if student_data[subject] < passing_marks
    ]

    if len(failed_subjects) == 0:
        st.success(
            f"PASS — {selected_student} passed all subjects."
        )
    else:
        st.error(
            f"FAIL — {selected_student} failed in: "
            + ", ".join(failed_subjects)
        )

    # -----------------------------
    # Student Performance Chart
    # -----------------------------
    st.subheader("Student Performance Chart")

    fig, ax = plt.subplots()

    ax.bar(
        subject_columns,
        [student_data[s] for s in subject_columns]
    )

    ax.axhline(
        passing_marks,
        linestyle="--",
        label="Pass Mark"
    )

    ax.set_ylabel("Marks")
    ax.set_xlabel("Subjects")
    ax.set_title(f"{selected_student}'s Performance")

    ax.legend()

    plt.xticks(rotation=30)
    plt.tight_layout()

    st.pyplot(fig)

    # -----------------------------
    # Select Subject
    # -----------------------------
    st.subheader("Subject Analysis")

    selected_subject = st.selectbox(
        "Select Subject",
        subject_columns
    )

    # -----------------------------
    # Subject-wise Statistics
    # -----------------------------
    st.write(f"### {selected_subject} Statistics")

    subject_marks = df[selected_subject]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average",
        f"{subject_marks.mean():.2f}"
    )

    col2.metric(
        "Highest",
        f"{subject_marks.max():.0f}"
    )

    col3.metric(
        "Lowest",
        f"{subject_marks.min():.0f}"
    )

    col4.metric(
        "Pass %",
        f"{(subject_marks >= passing_marks).mean() * 100:.1f}%"
    )

    # -----------------------------
    # Compare All Students
    # -----------------------------
    st.subheader("Compare All Students")

    comparison_df = df[
        [student_column] + subject_columns + ["Average"]
    ].copy()

    comparison_df = comparison_df.sort_values(
        "Average",
        ascending=False
    )

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # Average Comparison Chart
    # -----------------------------
    st.write("### Student Average Comparison")

    fig2, ax2 = plt.subplots()

    ax2.bar(
        comparison_df[student_column],
        comparison_df["Average"]
    )

    ax2.set_xlabel("Students")
    ax2.set_ylabel("Average Marks")
    ax2.set_title("Average Marks of All Students")

    plt.xticks(rotation=30)
    plt.tight_layout()

    st.pyplot(fig2)

else:
    st.info("Please upload a CSV file to begin.")