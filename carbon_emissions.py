import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd 
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import csv

def main():
    cal_or_bar = st.selectbox("Calculate Amount of Carbon Dioxide and Methane Emitted or Compare Carbon Emissions (Bar Graph)?", ["---Please select---","Compare Carbon Emissions (Bar Graph)", "Calculate Amount of Carbon Dioxide and Methane Emitted"])
    table = [] #preparing a list for appending
    with open("list_of_fuels.csv","r", encoding = "utf-8") as file: #open csv
        reader = csv.DictReader(file)
        for row in reader:
            table.append({"Fuel": row["Fuel"],
                        "Energy Content (MJ/kg)":row["Energy Content (MJ/kg)"], "Carbon Emissions (gCO₂/MJ)":row["Carbon Emissions (gCO₂/MJ)"]})
    st.subheader("Table: Fuel, Energy Content and Carbon Emissions")
    df = pd.DataFrame(table)
    st.dataframe(df)
    st.write("*Assumes green hydrogen. No direct CO₂ emissions upon use.")
    st.write("Note: ☘️ means it is a renewable energy!")

    if cal_or_bar == "Calculate Amount of Carbon Dioxide and Methane Emitted":
        st.subheader("Amount of Carbon Dioxide and Methane Emitted Calculator")
        amount_of_energy = st.number_input("Based on the table above or your own value, energy content of the fuel (MJ/kg):", min_value = 0.0)
        mass = st.number_input("Mass of the fuel consumed (kg): ", min_value = 0.0)
        carbon_emissions_cal = st.number_input("Based on the table above or your own value, carbon emissions (gCO₂/MJ): ", min_value = 0.0)
        if amount_of_energy == 0 or mass == 0:
            st.warning("Energy content and Mass cannot be 0!")
            return
        carbon_emitted = amount_of_energy * mass * carbon_emissions_cal
        st.info(f"{mass}kg of the fuel emitted {round(carbon_emitted/1000,3)}kg of CO₂.")
        st.info(f"🌳 To offset {round(carbon_emitted/1000,3)}kg of CO₂, you would need approximately {round(carbon_emitted/1000/26.635)} tree(s)!")
        methane_emissions_cal = st.number_input("Methane emissions in gCH4/MJ: ")
        methane_emitted = amount_of_energy * mass * methane_emissions_cal
        st.info(f"{mass}kg of the fuel emitted {round(methane_emitted/1000,3)}kg of CH₄.")
        st.info(f"💨 Over a 20-year period, methane is estimated to be 80 times more potent than CO₂ when it comes to warming the planet.\n Hence, the calculated amount of methane is equivalent to {round(methane_emitted/1000 * 80, 2)}  kg of CO₂.")

    if cal_or_bar == "Compare Carbon Emissions (Bar Graph)":
        table_substance = {}
        material_names = (name["Fuel"] for name in table)
        common_substance = st.multiselect(f"Please select one or more items from the list below:", material_names) #returns list
        st.subheader("Graph")

        if not common_substance:
            st.warning("To display the graph, please select at least one item from the table!")
            return
        for substance in common_substance: 
            for item in table:
                if substance == item["Fuel"]:
                    energy_content = float(item["Energy Content (MJ/kg)"])
                    carbon_emissions = float(item["Carbon Emissions (gCO₂/MJ)"])
                    table_substance[item["Fuel"]] = {"Energy Content (MJ/kg)": energy_content, "Carbon Emissions (gCO₂/MJ)": carbon_emissions}

        fig1, ax1 = plt.subplots(figsize = (12,6))
        renewable_energies = ["Hydrogen* (HHV)☘️", "Hydrogen* (LHV)☘️", "Vegetable Oil☘️", "Biodiesel☘️"] 

        fuel_names = list(table_substance.keys())
        colors = cm.get_cmap("tab20", len(fuel_names))
        fuel_color_map = {fuel: colors(i) for i, fuel in enumerate(fuel_names)}

        val_based = {k: v for k, v in sorted(table_substance.items(), key=lambda item:item[1]["Energy Content (MJ/kg)"])}
        for fuel, energy_con in val_based.items():
            Fuel = [fuel]
            Energy = [energy_con["Energy Content (MJ/kg)"]]
            energy_val = energy_con["Energy Content (MJ/kg)"]
            color = fuel_color_map[fuel]
            bars1 = ax1.bar(Fuel, Energy, width = 0.3, color=color)
            ax1.bar_label(bars1, label_type = "edge", color = "blue")

            if fuel in renewable_energies: #cannot use a list in ax.text!
                ax1.text(fuel, energy_val + 5, "☘️", ha = "center", fontsize = 20)

        #graph's info
        ax1.set_xlabel("Fuel")
        ax1.set_ylabel("Energy Content (MJ/kg)")
        ax1.tick_params(axis = "x", labelrotation=20)
        plot_title = st.text_input("Graph's title: ", key = "F")
        ax1.set_title(f"{plot_title}")
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots(figsize = (12,6))

        #table substance contains dicts within a dict, you need to specify which item in the 2nd dict to access 
        val_based = {k: v for k, v in sorted(table_substance.items(), key=lambda item:item[1]["Carbon Emissions (gCO₂/MJ)"])}

        for fuel, energy_con in val_based.items():
            Fuel = [fuel] #fuel gets the key, energy_con gets the value
            Energy2 = [energy_con["Carbon Emissions (gCO₂/MJ)"]]
            energy_2 = energy_con["Carbon Emissions (gCO₂/MJ)"]
            color = fuel_color_map[fuel]
            bars2 = ax2.bar(Fuel, Energy2, width = 0.3, color=color)
            ax2.bar_label(bars2, label_type = "edge", color = "blue")

            if fuel in renewable_energies: #cannot use a list in ax.text!
                ax2.text(fuel, energy_2 + 5, "☘️", ha = "center", fontsize = 20)

        #graph's info
        ax2.set_xlabel("Fuel")
        ax2.set_ylabel("Carbon Emissions (gCO₂/MJ)")
        ax2.tick_params(axis = "x", labelrotation=20)
        plot_title = st.text_input("Graph's title: ", key = "C")
        ax2.set_title(f"{plot_title}")
        st.pyplot(fig2)

main()