# CA Wastewater Virus Tracker

A real-time visualization dashboard for tracking viral loads in California wastewater, powered by the [CDPH Open Data API](https://data.ca.gov/dataset/wastewater-surveillance-data-california).

🔗 **Live Dashboard:** [https://tanvach.github.io/ca-wastewater-track/](https://tanvach.github.io/ca-wastewater-track/)

## 🚀 Features

*   **Multi-Virus Tracking**: Visualizes SARS-CoV-2, Influenza (A/B), RSV, Norovirus, Mpox, and more in a single consolidated chart.
*   **Adaptive Normalization**:
    *   Data is normalized to the **% of Peak in the Last 12 Months**.
    *   This allows impactful comparison between high-load viruses (like Norovirus) and low-load ones (like Respiratory viruses) without ancient outliers distorting recent trends.
*   **Smart Caching**:
    *   To prevent API throttling and improve load times, data is cached in the browser's `localStorage` for 24 hours.
    *   Data is compressed before storage to stay within browser quota limits.
*   **Interactive Visualization**:
    *   **7-Day Smoothing**: Reduces daily noise to show clear trends.
    *   **Click-to-Isolate**: Click a virus in the legend to hide all others and focus on that specific trend.
    *   **Recent Spikes**: Automatically detects and highlights the top 3 spiking viruses in the last 7 days.
*   **Kiosk Mode**:
    *   The dashboard automatically refreshes every 24 hours, making it ideal for always-on displays.

## 🛠️ Usage

This is a static HTML/JS application with no build steps required.

1.  Simply open `docs/index.html` in any modern web browser.
2.  Select your city/facility from the dropdown.

## 📡 Data Source

Data is sourced directly from the California Department of Public Health (CDPH) [CKAN API](https://data.ca.gov/api/3/action/package_show?id=cdph-wastewater-surveillance-data-california).

*   **Update Frequency**: The dashboard fetches live data on every load (unless cached).
*   **Privacy**: All processing happens client-side in your browser.

## 📦 GitHub Pages Deployment

This project is structured to be deployed via **GitHub Pages**:

1.  Push this repository to GitHub.
2.  Go to **Settings > Pages**.
3.  Under **Build and deployment**, select **Source: Deploy from a branch**.
4.  Select your branch (e.g., `main`) and set the folder to `/docs`.
5.  Save! Your site will be live.
