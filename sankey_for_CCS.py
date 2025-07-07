import streamlit as st
import plotly.graph_objects as go
import pandas as pd


st.title("Hello! New features yay.")


def climate_efforts():
    st.subheader("Carbon Capture & Storage (CCS) Simulation")
    volume = st.number_input("Volume of CO₂ produced at the facility in cubic meters (inclusive of amount released for compression and capture if applicable): ", min_value = 0.0)
    st.write("As the density of CO₂ varies with temperature and pressure, ")
    density = st.number_input("please enter an appropriate density that accounts for the actual temperature and pressure of the CO₂ in kg/m3: ", min_value = 0.0)
    total_mass = volume * density
    st.success(f"Total mass of CO₂ released from the plant: {total_mass/1000}metric tons, or {total_mass}kg")
    energy_source = st.selectbox("Compression and Capture Energy Source: ", ["---Please Select---", "Fossil Fuels of Same Plant", "External Clean Energy"])
   
    if energy_source == "---Please Select---":
        st.warning("Please select an energy source to proceed.")
        return
   
    percentage_for_capture = 0
    percentage_for_compress = 0


    if energy_source == "Fossil Fuels of Same Plant":
        percentage_for_compress = st.number_input("Energy required for compression (in % of total energy produced): ", min_value = 0.0, max_value=100.0)
        percentage_for_capture = st.number_input("Energy required for capture (in % of total energy produced): ", min_value = 0.0, max_value=100.0)    
   
    elif energy_source == "External Clean Energy":
        percentage_for_capture = 0
        percentage_for_compress = 0
        st.info("Since the energy is clean, it is assumed that no CO₂ is emitted in the capture and compression processes. ")


    compress = total_mass * percentage_for_compress/100
    st.success(f"CO₂ emitted during compression: {compress}kg")
    capture = total_mass * percentage_for_capture/100
    st.success(f"CO₂ emitted during capture: {capture}kg")
    main_process = total_mass - compress - capture
    st.success(f"CO₂ emitted from usable energy output: {main_process}kg")


    average_capture_rate = st.number_input("Average capture rate (efficiency) of the CCS facility (%): ", min_value=0.0, max_value=100.0)#use floats for both
    mass_not_captured_by_CCS = (100 - average_capture_rate)/100 * total_mass
    st.info(f"Uncaptured mass of CO₂: {mass_not_captured_by_CCS}kg")
   
    leakage = st.number_input("Estimated leakage percentage after capture: ", min_value=0.0, max_value=100.0)
    mass_leaked = leakage/100 * (total_mass - mass_not_captured_by_CCS)
    st.info(f"It is important to account for any CO₂ that may leak or be released during the capture, transportation, or storage process. Leaked mass of CO₂: {mass_leaked}kg ")
    st.success(f"Total uncaptured mass of CO₂: {mass_not_captured_by_CCS + mass_leaked}kg")
   
    co2_captured = total_mass - mass_not_captured_by_CCS - mass_leaked
    st.success(f"Mass of CO₂ successfully captured: {co2_captured/1000} metric tons, or {co2_captured}kg ")
    st.info(f"{co2_captured}kg is equivalent to the yearly emissions of {co2_captured/1000/4.6} cars. ")
   
    #sankey diagram
    dict_data_sankey = {"Total mass of CO₂ emitted by the plant": (total_mass), "CO₂ emitted during compression": (compress), "CO₂ emitted from capture process energy use": (capture), "CO₂ emitted from usable energy output": (main_process),
                    "Mass of CO₂ not captured by CCS": (mass_not_captured_by_CCS),
                   "Mass of CO₂ leaked": (mass_leaked), "Total mass of CO₂ captured": (co2_captured)}
    data_sankey=[]
    st.subheader("Table")
    for type in dict_data_sankey:
        data_sankey.append({"Flow Description": type, "CO₂ Mass (kg)": dict_data_sankey[type]})
    st.dataframe(data_sankey)
   
    source = [0, 1, 2] #splitting into 2 parts for tidiness
    target = [3, 3, 3] #if comma is placed at the end here, turns it into a tuple
    value = [compress, capture, main_process]


    source += [3, 3, 3] #appending elements from this list to the previous one ^ above
    target += [4, 5, 6]
    value += [mass_not_captured_by_CCS, mass_leaked, co2_captured]
   
    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 2),
      label = ["Compression Emissions", "Capture Emissions", "Usable Energy Output Emissions", "Total CO₂ Emitted", "Uncaptured CO₂", "Leaked CO₂", "Captured CO₂"],
                # 0 1 2 3 4 5 6
      color = ["red", "orange", "yellow", "black", "blue", "purple", "green"] #customising nodes
    ),
    # flow map: 0 --> 3, 1--> 3, 2--> 3 (converges to total CO₂ produced)
    # from 3, it then diverges to 4, 5, 6 (which is where the CO₂ ends up)
   
    link = dict(
      source = source, #cannot change the lists in place within the dictionary while defining them. So must do this!
      target = target,
      value = value,
      color = ["#ff6666", "#ff9966", "#ffff66",  #(all carbon emissions) #The total CO₂ emitted node (node 3) doesn't need its own link color(just a junction point).
           "#66b3ff", "#c266ff", "#66ff99"]  #(captured, uncaptured, leaked) #customising links
  ))])
    st.subheader("Sankey Diagram")
    fig.update_layout(font=dict(size = 20, color = "black"))
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Next Step: Geo-Sequestration")
    st.markdown("The carbon dioxide captured is compressed into a liquid and stored underground. \n\n Common storage sites include: \n 1. regions with porous rocks are favoured \n 2. saline water-saturated rocks \n3. depleted oil and gas fields \n4. coal seams")


climate_efforts()


