from io import BytesIO

import pandas as pd
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def create_pdf_report(df, quality):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            "FarmWise Insights Haryana",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "Filtered Agricultural Data Report",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            "DEMO DATA ONLY - Not official Haryana statistics.",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Records in report: {len(df)}",
            styles["Normal"]
        )
    )

    if not df.empty and "Production_Tonnes" in df.columns:
        elements.append(
            Paragraph(
                f"Total production: "
                f"{df['Production_Tonnes'].sum():,.2f} tonnes",
                styles["Normal"]
            )
        )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph("Data Quality Summary", styles["Heading2"])
    )

    quality_data = [
        ["Check", "Result"],
        ["Total records", str(quality["total_rows"])],
        ["Duplicate rows", str(quality["duplicate_rows"])],
        ["Missing cells", str(quality["missing_cells"])],
        ["Invalid numeric cells", str(quality["invalid_numeric_cells"])],
        ["Negative numeric values", str(quality["negative_values"])]
    ]

    quality_table = Table(
        quality_data,
        colWidths=[2.8 * inch, 2.0 * inch]
    )

    quality_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ])
    )

    elements.append(quality_table)
    elements.append(Spacer(1, 18))

    elements.append(
        Paragraph("Filtered Dataset Preview", styles["Heading2"])
    )

    preview = df.head(20).fillna("").copy()

    table_data = [preview.columns.astype(str).tolist()]

    for row in preview.itertuples(index=False, name=None):
        table_data.append([
            str(value)[:35] for value in row
        ])

    if len(table_data[0]) > 8:
        col_width = 10.0 * inch / len(table_data[0])
    else:
        col_width = 10.0 * inch / len(table_data[0])

    data_table = Table(
        table_data,
        colWidths=[col_width] * len(table_data[0]),
        repeatRows=1
    )

    data_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 6),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 3)
        ])
    )

    elements.append(data_table)

    document.build(elements)

    buffer.seek(0)
    return buffer.getvalue()


def render_reports_explorer(df):
    st.title("📊 Reports & Data Explorer")

    st.write(
        "Filter agricultural records, inspect data quality "
        "and download CSV or PDF reports."
    )

    st.warning(
        "The supplied dataset is demonstration data, "
        "not official Haryana statistics."
    )

    # ---------------------------
    # Filters
    # ---------------------------
    st.subheader("Filter Dataset")

    col1, col2, col3 = st.columns(3)

    years = sorted(df["Year"].dropna().unique().tolist())
    districts = sorted(df["District"].dropna().unique().tolist())
    crops = sorted(df["Crop"].dropna().unique().tolist())

    with col1:
        selected_years = st.multiselect(
            "Year",
            years,
            default=years,
            key="report_years"
        )

    with col2:
        selected_districts = st.multiselect(
            "District",
            districts,
            default=districts,
            key="report_districts"
        )

    with col3:
        selected_crops = st.multiselect(
            "Crop",
            crops,
            default=crops,
            key="report_crops"
        )

    filtered_df = df[
        df["Year"].isin(selected_years)
        & df["District"].isin(selected_districts)
        & df["Crop"].isin(selected_crops)
    ].copy()

    st.subheader("Filtered Records")

    st.metric("Records Found", len(filtered_df))

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------
    # Data quality checks
    # ---------------------------
    st.divider()
    st.subheader("🧪 Data Quality Checks")

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    numeric_data = df[numeric_columns]

    quality = {
        "total_rows": len(df),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "invalid_numeric_cells": int(
            numeric_data.isin([float("inf"), float("-inf")])
            .sum()
            .sum()
        ),
        "negative_values": int((numeric_data < 0).sum().sum())
    }

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Rows", quality["total_rows"])
    c2.metric("Duplicate Rows", quality["duplicate_rows"])
    c3.metric("Missing Cells", quality["missing_cells"])

    c4, c5 = st.columns(2)

    c4.metric(
        "Infinite Numeric Values",
        quality["invalid_numeric_cells"]
    )

    c5.metric(
        "Negative Numeric Values",
        quality["negative_values"]
    )

    missing_by_column = df.isna().sum()

    st.markdown("#### Missing Values by Column")

    st.dataframe(
        missing_by_column.rename("Missing Values"),
        use_container_width=True
    )

    if quality["missing_cells"] == 0 and quality["duplicate_rows"] == 0:
        st.success(
            "No missing cells or duplicate rows were detected."
        )
    else:
        st.warning(
            "Potential data quality issues were detected. "
            "Review the results before using the data."
        )

    if quality["invalid_numeric_cells"] > 0:
        st.warning(
            "Infinite numeric values were detected."
        )

    if quality["negative_values"] > 0:
        st.warning(
            "Negative numeric values were detected. "
            "Check whether they are valid for their columns."
        )

    # ---------------------------
    # CSV download
    # ---------------------------
    st.divider()
    st.subheader("⬇️ Download Reports")

    csv_bytes = filtered_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Download Filtered CSV",
        data=csv_bytes,
        file_name="farmwise_filtered_data.csv",
        mime="text/csv"
    )

    # ---------------------------
    # PDF download
    # ---------------------------
    pdf_bytes = create_pdf_report(
        filtered_df,
        quality
    )

    st.download_button(
        label="Generate and Download PDF Report",
        data=pdf_bytes,
        file_name="farmwise_agricultural_report.pdf",
        mime="application/pdf"
    )