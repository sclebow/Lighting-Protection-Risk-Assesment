import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from figure_utils import create_building_collection_figure
from report_utils import generate_csv_report, generate_odt_report
import pandas as pd

flash_density_map_url = "https://www.vaisala.com/sites/default/files/2020-09/Lightning/NLDN/LIFT-WEA-Lightning-NLDN-Map3-650x365.jpg"

st.set_page_config(
    page_title="NFPA 780 Lightning Risk Assessment",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None,
)

# Custom CSS to move sidebar to the right and reduce LaTeX font size
st.markdown(
    """
    <style>
    /* Reduce LaTeX font size in sidebar */
    [data-testid="stSidebar"] .katex-html {
        font-size: 0.85em !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("NFPA 780 Lightning Risk Assessment Calculator")
st.subheader("Author: Scott Lebow, P.E.")

st.markdown("""
This app calculates the risk of lightning strikes to a structure based on the NFPA 780 2026 simplified assessment method.
""")

project_name = st.text_input("Project Name", placeholder="Enter project name here")
tabs = st.tabs(["Simplified Assessment", "Detailed Assessment"])
with tabs[0]:
    st.subheader("Simplified Assessment")

    st.markdown("""
    This section provides a simplified assessment of lightning risk based on basic parameters.
    It is suitable for quick evaluations and does not cover all aspects of the NFPA 780 standard.
    """)

    st.markdown("---")
    st.markdown("##### Upload Project Data (optional)")
    uploaded_files = st.file_uploader(
        "Upload Project Data (optional)",
        type=["csv"],
        help="You can upload a CSV file with project data to pre-fill the input parameters. The file should have columns: 'Length', 'Width', 'Height', 'Ground Flash Density', 'Construction Coefficient', 'Contents Coefficient', 'Occupancy Coefficient', 'Consequence Coefficient'."
    )
    if uploaded_files:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_files)
        # Check if the required columns are present
        required_columns = [
            "Project Name",
            "Length (ft)",
            "Width (ft)",
            "Height (ft)",
            "Collection Area (m²)",
            "Ground Flash Density (flashes/sq miles/year)",
            "Expected Annual Threat Occurrence (flashes/year)",
            "Tolerable Lightning Frequency (flashes/year)",
            "Construction Coefficient",
            "Contents Coefficient",
            "Occupancy Coefficient",
            "Consequence Coefficient",
            "Location Coefficient",
            "LPS Recommendation",
        ]

        if all(col in df.columns for col in required_columns):
            # Pre-fill the input parameters with the first row of the DataFrame
            project_name = df.iloc[0]["Project Name"]
            l = float(df.iloc[0]["Length (ft)"])
            w = float(df.iloc[0]["Width (ft)"])
            h = float(df.iloc[0]["Height (ft)"])
            Ng = df.iloc[0]["Ground Flash Density (flashes/sq miles/year)"]
            C_2 = df.iloc[0]["Construction Coefficient"]
            C_3 = df.iloc[0]["Contents Coefficient"]
            C_4 = df.iloc[0]["Occupancy Coefficient"]
            C_5 = df.iloc[0]["Consequence Coefficient"]
            C_D = df.iloc[0]["Location Coefficient"]
            
            st.success("Project data loaded successfully!")
        else:
            st.error("Uploaded CSV file does not contain the required columns. Please check the file format.")
            # Set default values if the file is not valid
            l = 20.0
            w = 10.0
            h = 10.0
            Ng = ">0 to 4"
            C_2 = 1.0
            C_3 = 1.0
            C_4 = 1.0
            C_5 = 1.0
    else:
        # Default values for input parameters
        l = 20.0
        w = 10.0
        h = 10.0
        Ng = ">0 to 4"  # Default ground flash density
        C_2 = 1.0  # Default construction coefficient
        C_3 = 1.0
        C_4 = 1.0  # Default occupancy coefficient
        C_5 = 1.0

    st.markdown("---")

    # Input parameters
    st.markdown("### Input Parameters")    
    
    cols = st.columns(2, vertical_alignment="top")
    # Input parameters
    with cols[0]:
        st.markdown("#### Structure Dimensions")
        l = st.number_input("Length of structure (ft)", min_value=1.0, value=l)
        w = st.number_input("Width of structure (ft)", min_value=1.0, value=w)
        h = st.number_input("Height of structure (ft)", min_value=1.0, value=h)
        metric_fig_selection = st.radio(
            "Select Units for Visualization",
            ("Imperial (ft)", "Metric (m)"),
            index=0,
            horizontal=True
        )
        # Convert imperial units to metric
        l_m = l * 0.3048  # feet to meters
        w_m = w * 0.3048  # feet to meters
        h_m = h * 0.3048  # feet to meters
        # Calculate the collection area (A) in m²
        A_D = l_m * w_m + 6 * h_m * (l_m + w_m) + 9 * math.pi * h_m * h_m # Collection area in m²
        st.write(f"**Collection Area:** {A_D:.2f} m²")
        st.latex(r"A = l \times w + 6h(l + w) + 9\pi h^2 = \\{:.2f} \, \text{{m}} \times {:.2f} \, \text{{m}} + 6 \times {:.2f} \, \text{{m}} \, ( {:.2f} \, \text{{m}} + {:.2f} \, \text{{m}} ) + 9\pi \times ( {:.2f} \, \text{{m}} )^2 =\\ {:.2f} \, \text{{m}}^2".format(l_m, w_m, h_m, l_m, w_m, h_m, A_D))
        if metric_fig_selection == "Imperial (ft)":
            metric_fig = False
        else:
            metric_fig = True
    # 3D Visualization of Building and Collection Area (Interactive)
    with cols[1]:
        st.markdown("### Interactive 3D Visualization of Building and Collection Area")
        fig = create_building_collection_figure(l, w, h, metric=metric_fig)
        st.plotly_chart(fig)

    st.markdown("---")
    
    st.markdown("#### Ground Flash Density")

    # Display flash density map
    flash_ranges = {
        ">0 to 4": 2,
        "4 to 8": 6,
        "8 to 12": 10,
        "12 to 16": 14,
        "16 to 20": 18,
        "20 to 24": 22,
        "24 to 28": 26,
        "28 and up": 28
    }
    cols = st.columns(2)
    with cols[0]:
        st.image(flash_density_map_url, caption="Ground Flash Density Map", use_container_width=True)
    with cols[1]:
        Ng = st.selectbox(
            "Ground flash density (flashes/sq miles/year)",
            flash_ranges,
            index=0
        )

    st.markdown("---")
    st.markdown("#### Structure Construction Coefficient")
    # 3x3 grid input with unique selection
    row_names = ["Metal", "Nonmetallic", "Combustible"]
    col_names = ["Metal Roof", "Nonmmetallic Roof", "Combustible Roof"]
    values = [
        [0.5, 1.0, 2.0], # Metal Structure
        [1.0, 1.0, 2.5], # Nonmetallic Structure
        [2.0, 2.5, 3.0]  # Combustible Structure
    ]

    # Create a unique key for each cell
    cell_keys = [[f"cell_{i}_{j}" for j in range(3)] for i in range(3)]

    # Use session state to track the selected cell
    if "selected_cell" not in st.session_state:
        st.session_state.selected_cell = (0, 0)

    def select_cell(i, j):
        st.session_state.selected_cell = (i, j)

    st.markdown("##### Select a cell from the grid:")
    cols = st.columns([0.2, 0.2, 0.2, 0.2])  # extra col for row names

    # Header row
    cols[0].markdown("**Structure**")
    for j, col_name in enumerate(col_names):
        cols[j+1].markdown(f"**{col_name}**")

    for i, row_name in enumerate(row_names):
        cols = st.columns([0.2, 0.2, 0.2, 0.2])
        cols[0].markdown(f"**{row_name}**")
        for j in range(3):
            is_selected = (st.session_state.selected_cell == (i, j))
            button_label = f"{values[i][j]}"
            cols[j+1].button(
                button_label, 
                key=cell_keys[i][j], 
                help=f"{row_name} Structure - {col_names[j]}", 
                type="primary" if is_selected else "secondary",
                on_click=select_cell,
                args=(i, j)
            )

    selected_row, selected_col = st.session_state.selected_cell

    st.write(f"Selected cell: **{row_names[selected_row]} Structure - {col_names[selected_col]} - {values[selected_row][selected_col]}**")
    C_2 = values[selected_row][selected_col]

    st.markdown("---")
    st.markdown("#### Structure Location, Contents, Occupancy, and Lightning Consequence Coefficients")
    cols = st.columns(2, vertical_alignment="center")
    with cols[0]:
        structure_location_coefficients = {
            f"Structure surrounded by taller structures or trees within a distance of 3H ({3 * h}ft)": 0.25,
            f"Structure surrounded by structures of equal or lesser height within a distance of 3H ({3 * h}ft)": 0.5,
            f"Isolated structure, with no other structures located within a distance of 3H ({3 * h}ft)": 1.0,
            "Isolated structure on hilltop": 2.0
        }
        C_D = st.selectbox(
            "Relative Structure Location",
            list(structure_location_coefficients.keys()),
            index=0
        )
        C_D = structure_location_coefficients[C_D]
    with cols[1]:
        structure_contents_coefficients = {
            "Low value and noncombustible": 0.5,
            "Standard value and noncombustible": 1.0,
            "High value, moderate combustibility": 2.0,
            "Exceptional value, flammable liquids, computer or electronics": 3.0,
            "Exceptional value, irreplaceable cultural items": 4.0
        }
        C_3 = st.selectbox(
            "Detmination of Structure Contents Coefficient",
            list(structure_contents_coefficients.keys()),
            index=0
        )
        C_3 = structure_contents_coefficients[C_3]
    cols = st.columns(2, vertical_alignment="center")
    with cols[0]:
        structure_occupancy_coefficients = {
            "Unoccupied": 0.5,
            "Normally Occupied": 1.0,
            "Difficult to Evacuate or risk of panic": 3.0,
        }
        C_4 = st.selectbox(
            "Detmination of Structure Occupancy Coefficient",
            list(structure_occupancy_coefficients.keys()),
            index=0
        )
        C_4 = structure_occupancy_coefficients[C_4]
    with cols[1]:
        lighting_consequence_coefficients = {
            "Continuation of facility services not required, no environmental impact": 1.0,
            "Continuation of facility services required, no environmental impact": 5.0,
            "Consequences to the environment": 10.0,
        }
        C_5 = st.selectbox(
            "Detmination of Lightning Consequence Coefficient",
            list(lighting_consequence_coefficients.keys()),
            index=0
        )
        C_5 = lighting_consequence_coefficients[C_5]
    
    Ng = flash_ranges[Ng]  # Convert selected range to numeric value
    Ng_m2 = Ng * 0.386102  # Convert flashes/sq miles/year to flashes/sq km/year
    
    # Calculate the expected annual threat occurrence (N_D)
    N_D = Ng_m2 * A_D * C_D * 10**-6

    # Calculate the combined coefficient (C)
    C = C_2 * C_3 * C_4 * C_5
    
    # Calculate the tolerable lightning frequency (N_c)
    N_c = 1.5 * 10**-3 / C

    # If N_D <= N_c, a Lightning Protection System (LPS) is optional
    # If N_D > N_c, an LPS is recommended
    if N_D <= N_c:
        lps_boolean = True
        lps_recommendation = "A Lightning Protection System (LPS) is **optional**."
    else:
        lps_boolean = False
        lps_recommendation = "A Lightning Protection System (LPS) is **recommended**."

    # Set page background color based on recommendation
    if not lps_boolean:
        st.markdown(
            """
            <style>
            body, [data-testid="stAppViewContainer"] {
                background-color: #fffbe6 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            body, [data-testid="stAppViewContainer"] {
                background-color: #e6f0ff !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.header("Results")
    st.markdown("### Summary of Calculations")
    st.markdown("---")
    st.markdown(f"#### Coefficients")
    cols = st.columns(6)
    with cols[0]:
        st.markdown("**Construction Coefficient (C_2)**")
        st.latex(r"C_2 = {:.2f}".format(C_2))
    with cols[1]:
        st.markdown("**Contents Coefficient (C_3)**")
        st.latex(r"C_3 = {:.2f}".format(C_3))
    with cols[2]:
        st.markdown("**Occupancy Coefficient (C_4)**")
        st.latex(r"C_4 = {:.2f}".format(C_4))
    with cols[3]:
        st.markdown("**Consequence Coefficient (C_5)**")
        st.latex(r"C_5 = {:.2f}".format(C_5))
    with cols[4]:
        st.markdown("**Location Coefficient (C_D)**")
        st.latex(r"C_D = {:.2f}".format(C_D))
    with cols[5]:
        st.markdown("**Combined Coefficient (C)**")
        st.latex(r"C = C_2 \times C_3 \times C_4 \times C_5 =\\ {:.2f} \times {:.2f} \times {:.2f} \times {:.2f} = {:.2f}".format(C_2, C_3, C_4, C_5, C))
    st.markdown("---")
    st.markdown(f"#### Dimensions")
    cols = st.columns(3)
    with cols[0]:
        st.write(f"**Length of Structure (l):** {l:.2f} ft ({l_m:.2f} m)")
        st.latex(r"l = \\{:.2f} \, \text{{ft}} = {:.2f} \, \text{{m}}".format(l, l_m))
    with cols[1]:
        st.write(f"**Width of Structure (w):** {w:.2f} ft ({w_m:.2f} m)")
        st.latex(r"w = \\{:.2f} \, \text{{ft}} = {:.2f} \, \text{{m}}".format(w, w_m))
    with cols[2]:
        st.write(f"**Height of Structure (h):** {h:.2f} ft ({h_m:.2f} m)")
        st.latex(r"h = \\{:.2f} \, \text{{ft}} = {:.2f} \, \text{{m}}".format(h, h_m))
    st.write(f"**Collection Area:** {A_D:.2f} m²")
    st.latex(r"A = l \times w + 6h(l + w) + 9\pi h^2 = \\{:.2f} \, \text{{m}} \times {:.2f} \, \text{{m}} + 6 \times {:.2f} \, \text{{m}} \, ( {:.2f} \, \text{{m}} + {:.2f} \, \text{{m}} ) + 9\pi \times ( {:.2f} \, \text{{m}} )^2 =\\ {:.2f} \, \text{{m}}^2".format(l_m, w_m, h_m, l_m, w_m, h_m, A_D))
    st.markdown("---")
    st.write(f"**Ground Flash Density (Ng):** {Ng} flashes/sq miles/year ({Ng_m2:.2f} flashes/km²/year)")
    st.latex(r"N_g = \\{:.2f} \, \text{{flashes/sq miles/year}} = {:.2f} \, \text{{flashes/km}}^2/\text{{year}}".format(Ng, Ng_m2))
    st.write(f"**Expected Annual Threat Occurrence:** {N_D:.2e} flashes/year")
    st.latex(r"N_D = N_g \times A \times C_D \times 10^{{-6}} =\\ {:.2f} \times {:.2f} \times {:.2f} \times 10^{{-6}} = {:.6f}".format(Ng_m2, A_D, C_D, N_D))
    st.write(f"**Tolerable Lightning Frequency:** {N_c:.2e} flashes/year")
    st.latex(r"N_c = \frac{{1.5 \times 10^{{-3}}}}{{C}} = \frac{{1.5 \times 10^{{-3}}}}{{{:.2f}}} = {:.6f}".format(C, N_c))

    if lps_boolean:
        st.latex(r"N_D \leq N_c \Rightarrow \text{LPS is optional}")
    else:
        st.latex(r"N_D > N_c \Rightarrow \text{LPS is recommended}")

    st.markdown("---")

    st.markdown(f"## Lightning Protection System Recommendation")
    st.markdown(lps_recommendation)
    st.markdown("""
    **Note:** This is the simplified assessment based on the NFPA 780 standard. For a detailed assessment, please refer to the detailed assessment tab.
    """)
    # Prepare data for report
    report_data = {
        "Project Name": project_name,
        "Length (ft)": l,
        "Width (ft)": w,
        "Height (ft)": h,
        "Collection Area (m²)": A_D,
        "Ground Flash Density (flashes/sq miles/year)": Ng,
        "Expected Annual Threat Occurrence (flashes/year)": N_D,
        "Tolerable Lightning Frequency (flashes/year)": N_c,
        "Construction Coefficient": C_2,
        "Contents Coefficient": C_3,
        "Occupancy Coefficient": C_4,
        "Consequence Coefficient": C_5,
        "Location Coefficient": C_D,
        "LPS Recommendation": lps_recommendation,
    }
    csv_bytes = generate_csv_report(report_data)
    odt_bytes = generate_odt_report(report_data)

    now = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    cols = st.columns(2)
    with cols[0]:
        st.download_button(
            label="Download CSV Report",
            data=csv_bytes,
            file_name=f"{project_name}_lightning_risk_assessment_{now}.csv",
            mime="text/csv"
        )
    with cols[1]:
        st.download_button(
            label="Download OpenDocument Report",
            data=odt_bytes,
            file_name=f"{project_name}_lightning_risk_assessment_{now}.odt",
            mime="application/vnd.oasis.opendocument.text"
        )

with tabs[1]:
    st.subheader("Detailed Assessment")

    st.markdown("""
    This section provides a detailed assessment of lightning risk based on the NFPA 780 standard.
    It includes additional parameters and calculations for a more comprehensive evaluation.
    """)

    st.markdown("---")

    st.markdown("### Coming Soon")
    st.markdown("""
    The detailed assessment section is under development. Please check back later for updates.
    """)