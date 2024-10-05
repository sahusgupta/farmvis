import streamlit as st

def farm_information_form():
    st.title("🌾 Farm Information Form")
    with st.form(key='farm_form'):
        # Geographic Location
        st.header("📍 Geographic Location")
        address = st.text_input("Address")
        # Crops Grown
        st.header("🌱 Crops Grown")
        crops = st.multiselect(
            "Select the crops grown on your farm:",
            options=[
                "Wheat", "Corn", "Rice", "Soybeans", "Barley",
                "Oats", "Cotton", "Sugarcane", "Vegetables",
                "Fruits", "Other"
            ]
        )

        # Type of Farm
        st.header("🏡 Type of Farm")
        farm_type = st.selectbox(
            "Select the type of your farm:",
            options=[
                "Organic", "Conventional", "Mixed", "Dairy", "Poultry",
                "Aquaculture", "Viticulture", "Orchard", "Greenhouse",
                "Other"
            ]
        )

        # Size of the Farm
        st.header("📏 Size of the Farm")
        size = st.number_input(
            "Enter the size of your farm (in acres):",
            min_value=0.0,
            step=0.1,
            format="%.2f"
        )

        # Purpose of the Farm
        st.header("🎯 Purpose of the Farm")
        purpose = st.radio(
            "Select the primary purpose of your farm:",
            options=["Commercial", "Subsistence", "Research", "Educational", "Recreational"]
        )
        
        st.header("Type of Bugs")
        pest_type = st.text_input(
            "Note the bugs most frequently found in your area:",
        )

        # Submit Button
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Validate Inputs
        if not address:
            st.error("Please enter the city.")
        elif not crops:
            st.error("Please select at least one crop.")
        elif size <= 0:
            st.error("Please enter a valid farm size.")
        else:
            # Display Submitted Information
            st.success("✅ Farm information submitted successfully!")
            st.subheader("📄 Submitted Details:")
            st.write(f"**Crops Grown:** {', '.join(crops)}")
            st.write(f"**Type of Farm:** {farm_type}")
            st.write(f"**Size of the Farm:** {size} acres")
            st.write(f"**Purpose of the Farm:** {purpose}")
            st.session_state['info'] = [crops, purpose, farm_type, size, pest_type]
def main():
    farm_information_form()

if __name__ == '__main__':
    main()
