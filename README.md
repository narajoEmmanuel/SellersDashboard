# Streamlit Sellers Dashboard

This project is an interactive analytics dashboard built with **Streamlit**, designed to visualize and explore sales performance data from the `sellers.xlsx` dataset.  
It was developed as part of the *Web Development for Analytics Apps* module.

The dashboard includes:
- Overview metrics (vendors, total units, sales, averages)
- Interactive region filtering
- Altair visualizations for sales and units sold
- Vendor-specific breakdown
- Downloadable filtered data
- Clean sidebar with dataset info and navigation

---

## 🚀 Live App  
Access the deployed application on Streamlit Cloud:

🔗 **https://sellersdashboard-f6hwyburzs57ah3afm7zks.streamlit.app/**

---

## 📂 Repository Structure

- streamlit_emmanuelnaranjo.py # Main Streamlit application
- sellers.xlsx # Dataset used in the dashboard
- requirements.txt # Python dependencies
- run.sh # Startup script for Streamlit Cloud deployment


---

## 📊 Features

### ✔ Interactive Filters  
Filter the dataset by region and vendor dynamically.

### ✔ Professional Visualizations  
Altair charts displaying:
- Total Sales by Vendor  
- Units Sold by Vendor  
- Average Sales  

### ✔ Vendor Detail Panel  
Detailed vendor-specific insights including:
- Total Units  
- Total Sales  
- Sales Average (%)  
- Income  

### ✔ Data Export  
Download the filtered dataset directly from the interface.

---

## 🛠️ Technologies Used

- **Streamlit 1.51**
- **Pandas 2.2.2**
- **NumPy 1.26.4**
- **Altair 5.2.0**
- **Matplotlib 3.9.0**
- **Openpyxl** (Excel file handling)
- Python 3.13 on Streamlit Cloud

---

## ▶️ How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/streamlit-sellers-dashboard
   
2. Move into the project directory:
   ```bash
   cd streamlit-sellers-dashboard

4. Install requirements:
   ```bash
   pip install -r requirements.txt

6. Run the application:
   ```bash
   streamlit run streamlit_emmanuelnaranjo.py
---
## 📧 Author

- Emmanuel Naranjo
- Module: Web Development for Analytics Apps
- Tecnológico de Monterrey

---
## ✔ Notes

This project was created as part of an academic assignment focused on Streamlit development, Git/GitHub workflows, and cloud deployment.
All data originates from the provided sellers.xlsx file.
