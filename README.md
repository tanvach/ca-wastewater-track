# CA Wastewater Virus Tracker

A real-time visualization dashboard for tracking viral loads in California wastewater, powered by the [CDPH Open Data API](https://data.chhs.ca.gov/dataset/wastewater-surveillance-data-california).

🔗 **Live Dashboard:** [https://tanvach.github.io/ca-wastewater-track/](https://tanvach.github.io/ca-wastewater-track/)

## 🚀 Features

*   **Multi-Virus Tracking**: Visualizes SARS-CoV-2, Influenza (A/B), RSV, Norovirus, Mpox, and more in a single consolidated chart.
*   **Data Normalization**:
    *   The app supports normalizing viral counts by PMMoV (Pepper Mild Mottle Virus) to account for dilution.
    *   **Note**: PMMoV data is currently unavailable in the public CA Open Data set for many locations (including San Francisco), so the dashboard automatically falls back to **Raw Concentration** (copies/L).
*   **Adaptive Baseline**:
    *   Data is normalized to the **% of Peak in the Last 18 Months**.
    *   This allows meaningful comparison between high-load viruses (like Norovirus) and low-load ones (like COVID-19) without ancient outliers distorting recent trends.
*   **One Series per Line**:
    *   Some plants are tested by more than one lab, in units that can't be compared (e.g. copies/g of dry sludge vs copies/L of wastewater); some labs also sample upstream manholes, and some run more than one assay for the same virus.
    *   For each plant and virus the dashboard plots a single lab + unit + site + assay series, narrowing the candidates in order: still reporting (data within 14 days of the newest sample), then samples at the plant over unlabelled over upstream sites, then within 10% of the most sample days in the last 18 months, then the most all-time sample days. Same-day samples within the series are averaged.
*   **Non-Detects Count as Zero**:
    *   Samples where a virus wasn't found are plotted as 0, so a rare detection shows as a brief bump instead of being smoothed into a steady trend. Viruses with no detections in the selected range aren't drawn.
*   **Robust Smoothing Algorithm**:
    *   **Two-Step Filter**: Combines a 5-day rolling median (to remove single-day outliers) followed by a 7-day rolling average (to show clear trends).
    *   The median never turns a day with a detection into 0, so detections among mostly-zero samples stay visible. The trade-off: a one-off bad reading among non-detects isn't removed either, since it can't be told apart from a real rare detection.
    *   This approach is more resilient to data anomalies than simple averaging.
*   **Smart Caching**:
    *   To prevent API throttling and improve load times, data is cached in the browser's `localStorage` for 24 hours.
    *   Cache is intelligently normalized by city name, so switching between facilities in the same city is instant.
*   **Interactive Visualization**:
    *   **City Autocomplete**: Search and select from all available wastewater treatment facilities across California.
    *   **Click-to-Isolate**: Click a virus in the legend to hide all others and focus on that specific trend.
    *   **Enhanced Tooltips**: Hover over any data point to see the virus name and percentage in large, bold text.
    *   **Recent Trends**: Automatically displays the top 3 most active viruses with intensity indicators (Low/Elevated/High Activity).
*   **Kiosk Mode**:
    *   The dashboard automatically refreshes every 24 hours, making it ideal for always-on displays.
*   **Dark Mode**: Full dark mode support for comfortable viewing.
*   **Mobile Optimized**: Responsive design works on phones, tablets, and desktop.

## 🛠️ Usage

This is a static HTML/JS application with no build steps required.

1.  Simply open `docs/index.html` in any modern web browser.
2.  Select your city/facility from the dropdown.

## 📡 Data Source

Data is sourced directly from the California Department of Public Health (CDPH) [CKAN API](https://data.chhs.ca.gov/api/3/action/package_show?id=wastewater-surveillance-data-california) on the CalHHS Open Data Portal.

> [!IMPORTANT]
> **Dataset Limitations**: This dataset is a subset of the data collected by the [WastewaterSCAN](https://wastewaterscan.org/) project. Crucially, it **does not include PMMoV (fecal normalization) data** for many sites.
> While ideally all viral data should be normalized by PMMoV to account for rainfall and dilution, this open dataset forces the use of **Raw Viral Concentrations**. Trends remain accurate, but magnitudes may be affected by extreme weather events.

*   **Update Frequency**: The dashboard fetches live data on every load (unless cached).
*   **Privacy**: All processing happens client-side in your browser.

## 📦 GitHub Pages Deployment

This project is structured to be deployed via **GitHub Pages**:

1.  Push this repository to GitHub.
2.  Go to **Settings > Pages**.
3.  Under **Build and deployment**, select **Source: Deploy from a branch**.
4.  Select your branch (e.g., `main`) and set the folder to `/docs`.
5.  Save! Your site will be live.
