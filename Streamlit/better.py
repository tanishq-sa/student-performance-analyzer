import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Student Performance Analyzer",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("Student Performance Analyzer")
st.caption("Interactive student marks and performance analysis")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    st.divider()

    st.write("Settings")

    passing_marks = st.slider(
        "Passing Marks",
        min_value=0,
        max_value=100,
        value=40
    )


# --------------------------------------------------
# NO FILE
# --------------------------------------------------

if uploaded_file is None:

    st.info("Upload a CSV file from the sidebar to get started.")

    st.markdown("""
    ### Expected CSV format

    Your CSV should look something like:

    | Student | Math | Python | DBMS | AI |
    |---|---:|---:|---:|---:|
    | Rahul | 78 | 85 | 72 | 90 |
    | Priya | 65 | 74 | 80 | 76 |
    | Aman | 35 | 42 | 38 | 45 |
    | Sneha | 92 | 89 | 95 | 91 |

    **First column:** Student name  
    **Other numeric columns:** Subjects
    """)

    st.stop()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error(f"Unable to read CSV: {e}")
    st.stop()


# --------------------------------------------------
# BASIC VALIDATION
# --------------------------------------------------

if df.empty:

    st.error("The uploaded CSV is empty.")
    st.stop()


student_column = df.columns[0]

subject_columns = df.select_dtypes(
    include="number"
).columns.tolist()


if not subject_columns:

    st.error("No numeric subject columns were found.")

    st.stop()


# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

df["Average"] = df[subject_columns].mean(axis=1)

df["Total"] = df[subject_columns].sum(axis=1)

df["Passed Subjects"] = (
    df[subject_columns] >= passing_marks
).sum(axis=1)

df["Failed Subjects"] = (
    df[subject_columns] < passing_marks
).sum(axis=1)

df["Result"] = df["Failed Subjects"].apply(
    lambda x: "PASS" if x == 0 else "FAIL"
)

df["Rank"] = (
    df["Average"]
    .rank(method="min", ascending=False)
    .astype(int)
)


# --------------------------------------------------
# CLASS OVERVIEW
# --------------------------------------------------

st.subheader("Class Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Students",
    len(df)
)

col2.metric(
    "Subjects",
    len(subject_columns)
)

col3.metric(
    "Class Average",
    f"{df['Average'].mean():.2f}"
)

col4.metric(
    "Passed",
    int((df["Result"] == "PASS").sum())
)

col5.metric(
    "Failed",
    int((df["Result"] == "FAIL").sum())
)


# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Dataset",
    "Student Analysis",
    "Subject Analysis",
    "Class Comparison"
])


# ==================================================
# TAB 1 — DATASET
# ==================================================

with tab1:

    st.subheader("Dataset")

    search = st.text_input(
        "Search Student",
        placeholder="Type a student name..."
    )

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df[student_column]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    result_filter = st.multiselect(
        "Filter by Result",
        ["PASS", "FAIL"],
        default=["PASS", "FAIL"]
    )

    if result_filter:

        filtered_df = filtered_df[
            filtered_df["Result"].isin(result_filter)
        ]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    st.write(
        f"Showing {len(filtered_df)} students"
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Processed Dataset",
        data=csv,
        file_name="student_analysis.csv",
        mime="text/csv"
    )


# ==================================================
# TAB 2 — STUDENT ANALYSIS
# ==================================================

with tab2:

    st.subheader("Individual Student Analysis")

    selected_student = st.selectbox(
        "Select Student",
        df[student_column].tolist()
    )

    student = df[
        df[student_column] == selected_student
    ].iloc[0]

    # Student metrics

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Average",
        f"{student['Average']:.2f}"
    )

    col2.metric(
        "Total Marks",
        f"{student['Total']:.0f}"
    )

    col3.metric(
        "Rank",
        f"#{student['Rank']}"
    )

    col4.metric(
        "Result",
        student["Result"]
    )

    # Result

    if student["Result"] == "PASS":

        st.success(
            f"{selected_student} passed all subjects."
        )

    else:

        failed = [
            subject
            for subject in subject_columns
            if student[subject] < passing_marks
        ]

        st.error(
            f"{selected_student} failed in: "
            + ", ".join(failed)
        )

    # Individual marks

    st.write("### Individual Marks")

    marks_df = pd.DataFrame({
        "Subject": subject_columns,
        "Marks": [
            student[subject]
            for subject in subject_columns
        ]
    })

    st.dataframe(
        marks_df,
        use_container_width=True,
        hide_index=True
    )

    # Performance chart

    st.write("### Performance")

    fig = px.bar(
        marks_df,
        x="Subject",
        y="Marks",
        title=f"{selected_student}'s Subject Performance",
        text="Marks"
    )

    fig.add_hline(
        y=passing_marks,
        line_dash="dash",
        annotation_text="Passing Marks"
    )

    fig.update_layout(
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Radar chart

    st.write("### Performance Profile")

    radar = px.line_polar(
        marks_df,
        r="Marks",
        theta="Subject",
        line_close=True,
        range_r=[0, 100]
    )

    radar.update_traces(
        fill="toself"
    )

    st.plotly_chart(
        radar,
        use_container_width=True
    )


# ==================================================
# TAB 3 — SUBJECT ANALYSIS
# ==================================================

with tab3:

    st.subheader("Subject-wise Analysis")

    selected_subject = st.selectbox(
        "Select Subject",
        subject_columns,
        key="subject_selector"
    )

    subject_marks = df[selected_subject]

    # Subject metrics

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

    pass_percentage = (
        subject_marks >= passing_marks
    ).mean() * 100

    col4.metric(
        "Pass Percentage",
        f"{pass_percentage:.1f}%"
    )

    # Subject performance

    subject_df = pd.DataFrame({
        "Student": df[student_column],
        "Marks": df[selected_subject]
    })

    subject_df = subject_df.sort_values(
        "Marks",
        ascending=False
    )

    fig = px.bar(
        subject_df,
        x="Student",
        y="Marks",
        title=f"{selected_subject} Performance",
        text="Marks"
    )

    fig.add_hline(
        y=passing_marks,
        line_dash="dash",
        annotation_text="Passing Marks"
    )

    fig.update_layout(
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Statistics

    st.write("### Statistics")

    statistics = pd.DataFrame({
        "Statistic": [
            "Average",
            "Median",
            "Highest",
            "Lowest",
            "Standard Deviation",
            "Pass Percentage"
        ],

        "Value": [
            subject_marks.mean(),
            subject_marks.median(),
            subject_marks.max(),
            subject_marks.min(),
            subject_marks.std(),
            pass_percentage
        ]
    })

    st.dataframe(
        statistics,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# TAB 4 — CLASS COMPARISON
# ==================================================

with tab4:

    st.subheader("Compare All Students")

    ranking = df[
        [
            student_column,
            "Total",
            "Average",
            "Passed Subjects",
            "Failed Subjects",
            "Result",
            "Rank"
        ]
    ].sort_values(
        "Rank"
    )

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )

    # Average comparison

    st.write("### Average Comparison")

    comparison = df[
        [student_column, "Average"]
    ].sort_values(
        "Average",
        ascending=False
    )

    fig = px.bar(
        comparison,
        x=student_column,
        y="Average",
        text="Average",
        title="Student Average Comparison"
    )

    fig.add_hline(
        y=df["Average"].mean(),
        line_dash="dash",
        annotation_text="Class Average"
    )

    fig.update_layout(
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Pass / Fail

    st.write("### Pass / Fail Distribution")

    result_count = df["Result"].value_counts()

    fig2 = px.pie(
        values=result_count.values,
        names=result_count.index,
        title="Student Results",
        hole=0.4
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # Subject comparison

    st.write("### Subject Average Comparison")

    subject_average = pd.DataFrame({
        "Subject": subject_columns,
        "Average": [
            df[subject].mean()
            for subject in subject_columns
        ]
    })

    fig3 = px.bar(
        subject_average,
        x="Subject",
        y="Average",
        text="Average",
        title="Average Marks by Subject"
    )

    fig3.add_hline(
        y=passing_marks,
        line_dash="dash",
        annotation_text="Passing Marks"
    )

    fig3.update_layout(
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )