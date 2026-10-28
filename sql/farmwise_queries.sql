-- FarmWise Insights Haryana: starter SQL schema (SQL Server)
CREATE DATABASE FarmWiseInsights;
GO
USE FarmWiseInsights;
GO

CREATE TABLE CropProduction (
    RecordID INT IDENTITY(1,1) PRIMARY KEY,
    [Year] INT NOT NULL,
    District NVARCHAR(100) NOT NULL,
    Crop NVARCHAR(100) NOT NULL,
    Area_Hectares FLOAT NOT NULL,
    Yield_Tonnes_Per_Hectare FLOAT NOT NULL,
    Production_Tonnes FLOAT NOT NULL,
    Rainfall_mm FLOAT NULL,
    Average_Temperature_C FLOAT NULL,
    Indicative_Price_Rs_Per_Quintal FLOAT NULL
);
GO

-- Import data/haryana_crop_demo_data.csv using SSMS Import Flat File wizard.
-- DEMO DATA ONLY: replace with verified official data before reporting findings.

-- 1. Total production by crop
SELECT Crop, SUM(Production_Tonnes) AS TotalProductionTonnes
FROM CropProduction
GROUP BY Crop
ORDER BY TotalProductionTonnes DESC;

-- 2. District-wise production
SELECT District, SUM(Production_Tonnes) AS TotalProductionTonnes
FROM CropProduction
GROUP BY District
ORDER BY TotalProductionTonnes DESC;

-- 3. Yearly production trend
SELECT [Year], Crop, SUM(Production_Tonnes) AS ProductionTonnes
FROM CropProduction
GROUP BY [Year], Crop
ORDER BY [Year], Crop;

-- 4. Average yield by crop
SELECT Crop, AVG(Yield_Tonnes_Per_Hectare) AS AverageYield
FROM CropProduction
GROUP BY Crop
ORDER BY AverageYield DESC;

-- 5. Year-over-year change by crop (aggregate first, then compare)
WITH Yearly AS (
  SELECT [Year], Crop, SUM(Production_Tonnes) AS ProductionTonnes
  FROM CropProduction GROUP BY [Year], Crop
), Compared AS (
  SELECT [Year], Crop, ProductionTonnes,
         LAG(ProductionTonnes) OVER (PARTITION BY Crop ORDER BY [Year]) AS PreviousYearProduction
  FROM Yearly
)
SELECT [Year], Crop, ProductionTonnes, PreviousYearProduction,
       CASE WHEN PreviousYearProduction IS NULL OR PreviousYearProduction = 0 THEN NULL
            ELSE (ProductionTonnes - PreviousYearProduction) * 100.0 / PreviousYearProduction END AS YoYPercent
FROM Compared
ORDER BY Crop, [Year];
