import pandas as pd
import streamlit as st


def render_farmer_assistant(df):
    st.title("🌾 Farmer Assistant")
    st.write(
        "Explore crop information, agricultural data insights "
        "and answers to common farming questions."
    )

    st.warning(
        "This assistant uses demonstration data and general "
        "educational information. Verify farming decisions with "
        "local agricultural experts."
    )

    # Crop information
    st.subheader("🌱 Crop Information")

    crops = sorted(df["Crop"].dropna().unique().tolist())

    selected_crop = st.selectbox(
        "Select a crop",
        crops,
        key="assistant_crop"
    )

    crop_df = df[df["Crop"] == selected_crop]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Production",
        f"{crop_df['Production_Tonnes'].sum():,.0f} tonnes"
    )

    col2.metric(
        "Average Yield",
        f"{crop_df['Yield_Tonnes_Per_Hectare'].mean():.2f} tonnes/ha"
    )

    col3.metric(
        "Records Available",
        len(crop_df)
    )

    # General crop information
    crop_information = {
        "Wheat": (
            "Wheat is a cereal crop commonly grown during the "
            "Rabi season in Haryana. Variety selection, sowing "
            "time, irrigation and fertilizer management should "
            "follow local agricultural recommendations."
        ),
        "Rice": (
            "Rice is a cereal crop generally grown during the "
            "Kharif season. Water management, suitable varieties "
            "and local growing conditions are important."
        ),
        "Bajra": (
            "Bajra (pearl millet) is an important cereal crop "
            "known for its suitability to relatively dry "
            "conditions. Select varieties appropriate for the "
            "local climate and soil."
        ),
        "Cotton": (
            "Cotton is a fibre crop. Variety selection, pest "
            "monitoring and appropriate water management are "
            "important for crop management."
        ),
        "Mustard": (
            "Mustard is an oilseed crop commonly grown during "
            "the Rabi season. Sowing time and crop management "
            "depend on the variety and local conditions."
        )
    }

    st.info(
        crop_information.get(
            selected_crop,
            "Consult your local Krishi Vigyan Kendra for "
            "crop-specific information."
        )
    )

    st.subheader("📊 Dataset-Based Insights")

    district_production = (
        crop_df.groupby("District")["Production_Tonnes"]
        .sum()
        .sort_values(ascending=False)
    )

    if not district_production.empty:
        st.write(
            f"**Highest production in this dataset:** "
            f"{district_production.index[0]} "
            f"({district_production.iloc[0]:,.0f} tonnes)"
        )

        st.bar_chart(district_production)

    # Question and answer
    st.subheader("💬 Ask the Farmer Assistant")

    question = st.text_input(
        "Ask about crops, production, yield or rainfall",
        placeholder="Example: Which crop has the highest production?"
    )

    if st.button("Get Answer", key="farmer_answer_button"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            q = question.lower()

            if "highest production" in q or "most production" in q:
                result = (
                    df.groupby("Crop")["Production_Tonnes"]
                    .sum()
                    .sort_values(ascending=False)
                )

                st.success(
                    f"According to the current dataset, "
                    f"{result.index[0]} has the highest total "
                    f"production: {result.iloc[0]:,.0f} tonnes."
                )

            elif "highest yield" in q or "best yield" in q:
                result = (
                    df.groupby("Crop")["Yield_Tonnes_Per_Hectare"]
                    .mean()
                    .sort_values(ascending=False)
                )

                st.success(
                    f"{result.index[0]} has the highest average "
                    f"yield in this dataset: {result.iloc[0]:.2f} "
                    f"tonnes per hectare."
                )

            elif "rainfall" in q:
                rainfall = df["Rainfall_mm"].mean()

                st.success(
                    f"The average rainfall recorded in the "
                    f"current dataset is {rainfall:.1f} mm."
                )

            elif "temperature" in q:
                temperature = df["Average_Temperature_C"].mean()

                st.success(
                    f"The average temperature recorded in the "
                    f"current dataset is {temperature:.1f} °C."
                )

            elif "district" in q and (
                "highest" in q or "production" in q
            ):
                result = (
                    df.groupby("District")["Production_Tonnes"]
                    .sum()
                    .sort_values(ascending=False)
                )

                st.success(
                    f"{result.index[0]} has the highest total "
                    f"production in the current dataset: "
                    f"{result.iloc[0]:,.0f} tonnes."
                )

            elif any(crop.lower() in q for crop in crops):
                matching_crop = next(
                    crop for crop in crops if crop.lower() in q
                )

                result = df[df["Crop"] == matching_crop]

                st.info(
                    f"{matching_crop}: total recorded production "
                    f"is {result['Production_Tonnes'].sum():,.0f} "
                    f"tonnes, and average yield is "
                    f"{result['Yield_Tonnes_Per_Hectare'].mean():.2f} "
                    f"tonnes per hectare."
                )

            else:
                st.info(
                    "I can currently answer questions about "
                    "crop production, yield, districts, rainfall "
                    "and temperature. Please try one of these topics."
                )

    st.divider()

    # Agricultural resources
    st.subheader("📚 Agricultural Resources")

    st.markdown(
        "- [Haryana Agriculture Department]"
        "(https://agriharyana.gov.in/)"
    )

    st.markdown(
        "- [Indian Council of Agricultural Research (ICAR)]"
        "(https://icar.org.in/)"
    )

    st.markdown(
        "- [Krishi Vigyan Kendra Portal]"
        "(https://kvk.icar.gov.in/)"
    )

    st.caption(
        "Dataset figures are illustrative, not official "
        "Haryana agricultural statistics."
    )