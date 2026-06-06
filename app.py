import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Set up the page title
st.title("✨ RefineX: Smart Data Ingestion & Optimization Hub")
st.write("Welcome, Prasad! Drop your messy data file below to get started.")

# 2. Create the file uploader button
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

# 3. Check if a file has actually been uploaded
if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # --- NEW STEP 2 CODE STARTS HERE ---
    
    # 1. Read the file based on its extension
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    # 2. Display a sub-header
    st.subheader("Raw Data Preview")
    
    # 3. Show the interactive data table on the screen
    st.dataframe(df.head(10)) 
    
    # 4. Show basic info about the dataset size
    st.write(f"The dataset has **{df.shape[0]}** rows and **{df.shape[1]}** columns.")

    # --- NEW STEP 3 CODE STARTS HERE ---
    st.markdown("---") # Visual separator line
    st.subheader("📊 Data Health Check (Missing Values)")
    
    # 1. Calculate missing values per column
    missing_data = df.isnull().sum()
    
    # 2. Convert it into a clean DataFrame for plotting
    missing_df = pd.DataFrame({
        'Column Name': missing_data.index,
        'Missing Values Count': missing_data.values
    })
    
    # Filter to only show columns that actually have missing data
    missing_df = missing_df[missing_df['Missing Values Count'] > 0]
    
    if not missing_df.empty:
        st.warning("Uh oh! Found missing values in your dataset:")
        
        # 3. Create an interactive Plotly bar chart
        fig = px.bar(
            missing_df, 
            x='Column Name', 
            y='Missing Values Count',
            title='Missing Data Analysis',
            labels={'Missing Values Count': 'Number of Nulls'},
            template='plotly_dark' # Matches your slick dark theme!
        )
        
        # Display the chart on the Streamlit screen
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("Perfect! No missing values detected in this dataset. 🎉")

    # --- NEW STEP 4 CODE STARTS HERE ---
    st.markdown("---")
    st.subheader("🛠️ Data Cleaning Operations")
    
    # 1. Create a Sidebar for User Controls
    st.sidebar.header("Settings & Operations")
    
    # 2. Add an operation checkbox for removing duplicates
    remove_dupes = st.sidebar.checkbox("Remove Duplicate Rows", value=False)
    
    # 3. Add an operation selectbox for handling missing data
    missing_strategy = st.sidebar.selectbox(
        "Missing Values Strategy",
        ["Do Nothing", "Drop Missing Rows", "Fill with Zero", "Fill with Median/Mode"]
    )
    
    # 4. Trigger the cleaning process when clicking a button
    if st.button("🚀 Execute Smart Cleaning"):
        
        # Make a copy of our original data so we don't destroy it
        cleaned_df = df.copy()
        
        # Operation A: Handle Duplicates
        if remove_dupes:
            initial_count = cleaned_df.shape[0]
            cleaned_df = cleaned_df.drop_duplicates()
            final_count = cleaned_df.shape[0]
            st.info(f"Removed **{initial_count - final_count}** duplicate rows.")
            
        # Operation B: Handle Missing Values based on selection
        if missing_strategy == "Drop Missing Rows":
            cleaned_df = cleaned_df.dropna()
            st.info("Dropped rows containing missing numbers.")
            
        elif missing_strategy == "Fill with Zero":
            # For numeric columns fill with 0, for text columns fill with "Missing"
            numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(0)
            
            non_numeric_cols = cleaned_df.select_dtypes(exclude=['number']).columns
            cleaned_df[non_numeric_cols] = cleaned_df[non_numeric_cols].fillna("Missing")
            st.info("Filled empty slots with zero / 'Missing' place-holders.")
            
        elif missing_strategy == "Fill with Median/Mode":
            # Advanced: fill numbers with median, text with mode (most frequent)
            for col in cleaned_df.columns:
                if cleaned_df[col].dtype in ['int64', 'float64']:
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())
                else:
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mode()[0] if not cleaned_df[col].mode().empty else "Missing")
            st.info("Applied intelligent median/mode substitution.")

        # 5. Display the final cleaned result to the user
        st.subheader("✨ Cleaned Data Preview")
        st.dataframe(cleaned_df.head(10))
        st.success(f"Final Cleaned Dataset Size: **{cleaned_df.shape[0]}** rows and **{cleaned_df.shape[1]}** columns.")
        
        # --- NEW STEP 5 CODE STARTS HERE ---
        st.markdown("---")
        st.subheader("📥 Export Cleaned Report")
        
        # 1. Convert our clean DataFrame into a standard CSV string
        # index=False ensures Python doesn't add an annoying extra row-number column!
        csv_data = cleaned_df.to_csv(index=False).encode('utf-8')
        
        # 2. Create the actual interactive download button
        st.download_button(
            label="💾 Download Cleaned Data CSV",
            data=csv_data,
            file_name="prasad_cleaned_report.csv",
            mime="text/csv"
        )