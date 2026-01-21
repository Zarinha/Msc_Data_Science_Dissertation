# MSc Data Science Dissertation  

## 📘 Dissertation Project  
### **Viability of Sugarcane Ethanol Production and Export from Mozambique, South Africa, and Kenya to Europe**  
#### *A Comparative Predictive Analysis Using Brazil’s Ethanol Export Model to Sweden*  

---

## 👩‍🎓 Author  
- **Student:** Jessica Z  
- **Programme:** MSc Data Science (UEL-DS-7010 Dissertation)  
- **Institution:** University of East London  
- **Supervisor:** *[Name]*  
- **Submission Date:** 2025  

---

## 🧭 Project Overview  

This dissertation evaluates the **technical, economic, and environmental viability** of producing and exporting **sugarcane-based ethanol** from **Mozambique, South Africa, and Kenya** to **Europe**, using **Brazil’s ethanol export model to Sweden** as a comparative benchmark.  

The study integrates **predictive modeling**, **economic simulation**, **life-cycle assessment (LCA)**, and **policy analysis** to assess whether African ethanol production can contribute meaningfully to Europe’s renewable fuel transition under **EU RED II (2030)** sustainability requirements.  

The research provides a **data-driven decision framework** for policymakers and investors assessing alternative biofuel supply chains for Europe.

---

## 🧠 Research Question  

> **What is the viability of sugarcane ethanol production and export from Mozambique, South Africa, and Kenya to Europe, compared to Brazil’s export model to Sweden?**

---

## 🧩 Hypotheses Tested  

| ID | Hypothesis | Focus |
|----|------------|-------|
| **H1** | Sugarcane production in Mozambique, South Africa, and Kenya is climatically and agronomically viable. | Production feasibility |
| **H2** | Export economics are competitive with Brazil’s ethanol model under comparable logistics and trade assumptions. | Cost competitiveness |
| **H3** | Sugarcane ethanol meets or exceeds EU RED II 2030 greenhouse-gas reduction thresholds. | Environmental performance |
| **H4** | Ethanol remains a viable decarbonization pathway relative to electric vehicles given alcohol fuel availability. | Scenario comparison |
| **H5** | Large-scale ethanol adoption in Europe depends on access to flex-fuel vehicle technology developed in Brazil/Sweden. | Policy & technology readiness |

---

## ⚙️ Methodological Framework  

| Hypothesis | Method | Tools | Key Outputs |
|------------|--------|-------|-------------|
| **H1** | Regression & yield prediction | Python (Pandas, Scikit-Learn) | Predicted yields, production costs |
| **H2** | Monte Carlo simulation | Python (NumPy, SciPy) | Cost distributions & risk analysis |
| **H3** | Life Cycle Assessment (LCA) | OpenLCA, Python | CO₂-eq per liter & RED II compliance |
| **H4** | Comparative scenario modeling | Python, Excel | Ethanol vs EV emissions trajectories |
| **H5** | Policy mapping & SWOT analysis | Qualitative analysis | EU readiness assessment |

---

## 📊 Repository Structure  

> **Note:** Large raw climate datasets are intentionally excluded from version control due to GitHub file-size limits.

| Folder | Description |
|-------|-------------|
| 📁 `/data/processed` | Cleaned and aggregated datasets used in modeling |
| 📁 `/code` | Python scripts for preprocessing, modeling, and analysis |
| 🧮 `/models` | Model scripts and simulation code (e.g., Monte Carlo, regression outputs) |
| 📓 `/notebooks` | Jupyter notebooks for hypotheses H1–H5 (where applicable) |
| 📝 `/chapters` | Final dissertation chapters and supporting documents |
| 📈 `/figures` | Final plots, charts, and visual outputs |
| 📚 `/references` | Bibliography and academic sources |

---

## 🗂️ Data Availability  

- Raw climate data (`.nc`, NetCDF) from CRU and other public sources are **not included** due to file-size constraints.  
- To reproduce results:
  1. Download CRU TS datasets from the official provider  
  2. Place files in `data/raw/`  
  3. Run preprocessing and modeling scripts from `/code` and `/models`

All processed datasets required for reproducing results are included.

---

## ✅ Project Status  

| Stage | Status |
|------|--------|
| 📘 Proposal | ✅ Completed |
| 📚 Literature Review | ✅ Completed |
| 🧮 Predictive & Economic Modeling (H1–H3) | ✅ Completed |
| ⚙️ Scenario & Policy Analysis (H4–H5) | ✅ Completed |
| 📝 Writing & Review | ✅ Completed |
| 🎯 Final Submission | ✅ Submitted |

---

## 🧪 Reproducibility  

Install dependencies:

```bash
pip install -r requirements.txt
