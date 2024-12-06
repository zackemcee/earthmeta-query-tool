# EarthMeta Query Tool

## Overview
The **EarthMeta Query Tool** is a web-based application that allows users to query and explore data from the EarthMeta ecosystem. It provides features for filtering, sorting, and exporting data related to countries, cities, and lands.

## Features
- **Load Countries**: Displays a table of countries with details such as:
  - Country name
  - President's name
  - Rank
  - Latitude and Longitude
  - President's ID (UUID)
  
- **Filter by President**: 
  - Autocomplete feature to filter by President's name.
  - Automatically updates the User ID field with the corresponding President's UUID.

- **Load Cities**: Fetches and displays cities associated with the selected President or provided User ID.

- **Load Lands**: Fetches and displays detailed information about lands within the cities associated with the selected President or provided User ID.

- **Export to Excel**: Allows exporting the currently displayed table (countries, cities, or lands) as an Excel file.

- **Sorting**: Enables sorting of table columns by clicking on headers, with arrows indicating ascending or descending order.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Data Export**: XLSX.js library

## How to Use
1. **Filter Data**:
   - Use the **"Filter by President Name"** field to search for a President by name.
   - The corresponding **President's ID (UUID)** is automatically populated in the **User ID** field.

2. **Load Data**:
   - Click **"Load Countries"** to display the full list of countries.
   - Use **"Load Cities"** or **"Load Lands"** to retrieve city or land data based on the **User ID**.

3. **Export Data**:
   - Click **"Export to Excel"** to download the currently displayed table.
