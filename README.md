# FarmWise Insights Haryana
**Agriculture Data Analytics starter project — SQL Server + Python + Power BI**

## Important data note
The included CSV contains **synthetic illustrative demo data**, created only to help you build and test the project. It is **not official Haryana government data** and must not be presented as real findings. Replace it with verified official data before your final report or presentation.

## Project objectives
- Compare crop production and yield across districts and years.
- Explore relationships between crop production, area, rainfall, temperature and indicative prices.
- Build an interactive Power BI dashboard.
- Prepare a foundation for later NLP farmer-query analysis and deep-learning image classification.

## Folder contents
- `data/haryana_crop_demo_data.csv` — demo crop dataset
- `data/farmer_queries_sample.csv` — sample farmer queries for a future NLP module
- `sql/farmwise_queries.sql` — SQL Server database schema and analysis queries
- `python/analyze_data.py` — data checks, summary analysis and trend chart

## Start with Python
Install Python packages:
```bash
pip install pandas matplotlib
```
Run from the project folder:
```bash
python python/analyze_data.py
```
The script prints summary statistics and saves a trend chart to `output/production_trend.png`.

## Import into SQL Server
1. Open SQL Server Management Studio (SSMS) and connect to your local SQL Server.
2. Open `sql/farmwise_queries.sql` and execute the script to create the database/table.
3. Use **Tasks → Import Data** or **Import Flat File** to import the CSV into `dbo.CropProduction`.
4. If the wizard creates a separate table, map/rename columns to match the schema. Avoid running the create-table import twice.
5. Run the included analysis queries.

## Build the Power BI report
1. Open Power BI Desktop → **Get data → Text/CSV**.
2. Select `data/haryana_crop_demo_data.csv` and load it.
3. Add slicers for `Year`, `District`, and `Crop`.
4. Add KPI cards:
   - Total Production = `SUM(CropProduction[Production_Tonnes])`
   - Total Area = `SUM(CropProduction[Area_Hectares])`
   - Average Yield = `AVERAGE(CropProduction[Yield_Tonnes_Per_Hectare])`
5. Add visuals:
   - Line chart: Year vs Production_Tonnes; legend = Crop
   - Bar chart: District vs Production_Tonnes
   - Clustered bar/column: Crop vs Average Yield
   - Scatter chart: Rainfall_mm vs Yield_Tonnes_Per_Hectare; legend = Crop
   - Table: Year, District, Crop, Area, Yield, Production
6. Use a dark blue/green theme inspired by the reference dashboard. Add a clear note that the dataset is demo data until official data is loaded.

## Useful Power BI measures
```DAX
Total Production (Tonnes) = SUM(CropProduction[Production_Tonnes])
Total Area (Hectares) = SUM(CropProduction[Area_Hectares])
Average Yield (Tonnes/Ha) = AVERAGE(CropProduction[Yield_Tonnes_Per_Hectare])
Average Rainfall (mm) = AVERAGE(CropProduction[Rainfall_mm])
Average Temperature (°C) = AVERAGE(CropProduction[Average_Temperature_C])
```

## Recommended final dashboard layout
Top: title + year/district/crop slicers
Row 1: Total Production, Total Area, Average Yield, Average Rainfall
Middle: Production trend line chart, production by district, top crops
Bottom: yield comparison, rainfall-vs-yield scatter, detailed data table

## Next phase: NLP + Deep Learning
- NLP: classify farmer queries by crop, symptom, intent and language. Use real, permissioned/verified query data; the sample CSV is only illustrative.
- Deep Learning: train a CNN using a properly labeled crop-leaf image dataset for disease classification. Evaluate on held-out images and show uncertainty; do not treat predictions as a definitive diagnosis.
- Integrate the modules into the same web app only after the analytics dashboard works.
