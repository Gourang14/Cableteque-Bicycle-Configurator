"""
A Streamlit application for generating bicycle permutations from Excel files.
This version uses the original data processing logic and pairs it with a unique, 
modern user interface, featuring advanced searchable filters.
"""

from typing import Dict, List
import streamlit as st
import pandas as pd
import itertools
import json

st.set_page_config(page_title="Bike Configurator Pro", page_icon="🚴‍♂️", layout="wide", initial_sidebar_state="expanded")

def generate_bicycles_from_sheets(sheets: Dict[str, pd.DataFrame], id_separator: str = "-", precedence: str = "designator_order") -> List[Dict[str, str]]:
    """
    Generate bicycle permutations from a dict of pandas DataFrames. 
    (This is the original, unmodified logic from the provided script).
    """
    if "ID" not in sheets:
        raise ValueError("Excel file must contain a sheet named 'ID'")

    id_df = sheets["ID"].astype(object)
    designator_names = list(id_df.columns)

    lists_of_values = []
    for col in designator_names:
        vals = [str(v) for v in id_df[col].tolist() if pd.notna(v)]
        lists_of_values.append(vals)

    general = {}
    if "GENERAL" in sheets:
        gen_df = sheets["GENERAL"].astype(object)
        if gen_df.shape[0] >= 1:
            row = gen_df.iloc[0]
            for k, v in row.items():
                if pd.notna(v):
                    general[str(k)] = str(v)

    designator_sheet_map: Dict[str, pd.DataFrame] = {}
    for sheet_name, df in sheets.items():
        if sheet_name in ("ID", "GENERAL"):
            continue
        if df.shape[1] < 1:
            continue
        first_col_name = df.columns[0]
        designator_sheet_map[first_col_name] = df.astype(object)

    if any(len(vals) == 0 for vals in lists_of_values):
        return []

    combos = list(itertools.product(*lists_of_values))
    bicycles: List[Dict[str, str]] = []

    if precedence == "designator_order":
        sheet_application_order = ("designator_order", designator_names)
    else:
        sheet_application_order = ("sheet_priority", list(designator_sheet_map.keys()))

    for combo in combos:
        parts = [str(p) for p in combo]
        bike_id = id_separator.join(parts)
        bike: Dict[str, str] = {"ID": bike_id}
        bike.update(general)

        if sheet_application_order[0] == "designator_order":
            for i, designator_value in enumerate(combo):
                designator_name = designator_names[i]
                if designator_name not in designator_sheet_map:
                    continue
                df = designator_sheet_map[designator_name]
                first_col = df.columns[0]
                mask = df[first_col].astype(str) == str(designator_value)
                matched = df[mask]
                if matched.shape[0] == 0:
                    continue
                for _, row in matched.iterrows():
                    for col in df.columns[1:]:
                        val = row[col]
                        if pd.isna(val):
                            continue
                        bike[str(col)] = str(val)
        else:
            for sheet_designator_name in sheet_application_order[1]:
                if sheet_designator_name not in designator_names:
                    continue
                idx = designator_names.index(sheet_designator_name)
                chosen_value = combo[idx]
                df = designator_sheet_map[sheet_designator_name]
                first_col = df.columns[0]
                mask = df[first_col].astype(str) == str(chosen_value)
                matched = df[mask]
                if matched.shape[0] == 0:
                    continue
                for _, row in matched.iterrows():
                    for col in df.columns[1:]:
                        val = row[col]
                        if pd.isna(val):
                            continue
                        bike[str(col)] = str(val)

        bicycles.append(bike)

    return bicycles

st.title(" Bicycle Configurator")
st.markdown("An advanced tool to generate product permutations from specification sheets.")

st.sidebar.header("⚙️ Controls & Settings")
uploaded_file = st.sidebar.file_uploader(
    "Upload Your Bicycle Excel File",
    type=["xlsx"],
    help="The .xlsx file should contain 'ID', 'GENERAL', and component sheets."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Generation Options")
id_separator = st.sidebar.text_input("ID Separator", value="-", help="Character to join ID parts, e.g., '-'")
precedence = st.sidebar.radio(
    "Attribute Conflict Resolution",
    options=["designator_order", "sheet_priority"],
    format_func=lambda x: "By ID Column Order" if x == "designator_order" else "By Sheet Name Order",
    help="Determines which data takes precedence if attributes are defined in multiple places."
)

if uploaded_file is None:
    st.info("Welcome! Please upload your Excel file using the sidebar to begin.")
else:
    try:
        with st.spinner("Reading and parsing Excel file..."):
            xls_sheets = pd.read_excel(uploaded_file, sheet_name=None, dtype=str, engine="openpyxl")
        
        st.success(f"File processed successfully! Found sheets: `{'`, `'.join(xls_sheets.keys())}`")

        with st.spinner("Generating all possible bicycle permutations..."):
            bicycles = generate_bicycles_from_sheets(xls_sheets, id_separator=id_separator, precedence=precedence)

        if not bicycles:
            st.warning("No permutations were generated. Please check the 'ID' sheet in your file to ensure all columns have at least one value.")
        else:
            df_bikes = pd.DataFrame(bicycles)
            desired_order = [
                "ID", "Manufacturer", "Type", "Frame type", "Frame material", "Brake type", 
                "Brake warranty", "Operating temperature", "Wheel diameter", "Recommended height", 
                "Frame height", "Groupset manufacturer", "Groupset name", "Gears", 
                "Has suspension", "Suspension travel", "Frame color", "Logo"
            ]
            
            actual_columns = df_bikes.columns.tolist()
            new_order = [col for col in desired_order if col in actual_columns]
            new_order.extend([col for col in actual_columns if col not in new_order])
            df_bikes = df_bikes[new_order]
            
            bicycles_ordered = df_bikes.to_dict(orient='records')

            st.header(f" Generated {len(bicycles_ordered):,} Total Configurations")
            
            tab_view, tab_filter, tab_download = st.tabs([" View All Data", "🔍 Filter & Explore", " Download Center"])

            with tab_view:
                st.subheader("Complete Data Table")
                st.dataframe(df_bikes, use_container_width=True)

            with tab_filter:
                st.subheader("Dynamic Search & Filter")
                st.write("Select an attribute and then search for a specific value to filter the results.")
                
                filter_col = st.selectbox(
                    "Filter by Attribute:",
                    options=df_bikes.columns,
                    help="Choose the data field you want to filter on."
                )

                unique_values = sorted(df_bikes[filter_col].dropna().unique().tolist())

                filter_val = st.selectbox(
                    f"Search for a Value in '{filter_col}':",
                    options=unique_values,
                    help="Click and start typing to search for a value."
                )

                if filter_val:
                    filtered_df = df_bikes[df_bikes[filter_col] == filter_val]
                    st.write(f"Found **{len(filtered_df)}** configurations matching your criteria:")
                    st.dataframe(filtered_df)

            with tab_download:
                st.subheader("Export Full Dataset")
                
                col1, col2 = st.columns(2)

                json_bytes = json.dumps(bicycles_ordered, ensure_ascii=False, indent=4).encode("utf-8")
                col1.download_button(
                    label="Download as JSON",
                    data=json_bytes,
                    file_name="bicycle_configurations.json",
                    mime="application/json",
                    use_container_width=True
                )

                csv_bytes = df_bikes.to_csv(index=False).encode("utf-8")
                col2.download_button(
                    label="Download as CSV",
                    data=csv_bytes,
                    file_name="bicycle_configurations.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
        st.exception(e)


#credits

st.markdown("---")

st.markdown("**Special thanks to the Cableteque team for their support and feedback.**")

LINKEDIN_URL = "https://www.linkedin.com/in/gourang4/"
st.markdown(f"LinkedIn: {LINKEDIN_URL}")

