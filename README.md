# 🗺️ Geospatial Logistics & Route Optimization
### Last-Mile Delivery Intelligence for São Paulo E-Commerce (Olist Dataset)

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn)
![Folium](https://img.shields.io/badge/Folium-Mapping-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Complete-success)

---

## 📌 Project Overview


**Figure 1:** Final optimized fleet routing network across São Paulo using Greedy Nearest Neighbor Heuristic.
<img width="1238" height="593" alt="Screenshot 2026-05-27 201850" src="https://github.com/user-attachments/assets/242a218f-e66e-45dd-abe1-d95f70a13075" />


This project implements an end-to-end **Data Science** and **Operations Research (OR)** solution to optimize last-mile logistics distribution in São Paulo, Brazil. Using real-world transactional data from the **Olist Brazilian E-Commerce Dataset**, it solves two critical operational challenges faced by logistics companies:

- **Fleet Zone Allocation** — How should delivery zones be divided across available trucks?
- **Route Distance Minimization** — What is the most efficient visiting sequence to minimize total travel distance?

The solution combines **unsupervised machine learning** (K-Means Clustering) with a **combinatorial optimization heuristic** (Greedy Nearest Neighbor) to produce a fully actionable, map-visualized routing plan.

---

## 🎯 Business Problem

Last-mile delivery accounts for **53% of total shipping costs** in e-commerce logistics (Capgemini Research, 2019). Inefficient routing directly translates to:

| Problem | Business Impact |
|:--------|:----------------|
| Overlapping delivery zones | Wasted fuel & driver hours |
| Suboptimal visit sequences | Excessive mileage per route |
| No data-driven zone planning | Unbalanced workload across fleet |
| Manual route assignment | High operational cost & human error |

> **Objective:** Minimize total fleet travel distance across all routes while ensuring balanced workload distribution among 5 trucks operating in São Paulo.

---

## 🛠️ System Architecture & Methodology

### Pipeline Overview

```
Raw Geolocation Data (CSV)
         │
         ▼
┌─────────────────────┐
│  Data Ingestion &   │  → Filter São Paulo coordinates
│  Cleaning           │  → Remove duplicate entries
│                     │  → Sample 50 active delivery points
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Spatial Clustering │  → K-Means (k=5 clusters)
│  K-Means Algorithm  │  → Assign each point to nearest centroid
│                     │  → Balanced zone segmentation
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  VRP Optimization   │  → Greedy Nearest Neighbor Heuristic
│  Route Sequencing   │  → Per-cluster route construction
│                     │  → Hub → Stops → Hub
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Interactive Map    │  → Folium PolyLine visualization
│  Visualization      │  → Color-coded routes per truck
│                     │  → Exportable HTML output
└─────────────────────┘
```

---

### 1. Mathematical Formulation

**Objective Function — Minimize Total Fleet Distance:**

$$\min Z = \sum_{k=1}^{K} \sum_{i=0}^{N} \sum_{j=0}^{N} d_{ij} \cdot x_{ijk}$$

**Where:**
- $K$ = total number of trucks (fleet size)
- $N$ = total number of delivery points
- $d_{ij}$ = geodesic distance between point $i$ and point $j$
- $x_{ijk} \in \{0, 1\}$ = 1 if truck $k$ travels directly from $i$ to $j$

**Model Constraints:**
- Every delivery point $i$ must be visited **exactly once** by exactly one truck
- Every truck route must **start and end** at the Main Distribution Hub ($i = 0$)
- Distance $d_{ij}$ is computed using the **Haversine Formula** for geodesic accuracy

---

### 2. Haversine Distance Formula

To accurately measure real-world distances between geographic coordinates on Earth's curved surface:

$$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)$$

**Parameters:**
| Symbol | Description |
|:------:|:------------|
| $\phi$ | Latitude in radians |
| $\lambda$ | Longitude in radians |
| $R$ | Earth's radius = **6,371 km** |
| $\Delta\phi$ | Latitude difference between two points |
| $\Delta\lambda$ | Longitude difference between two points |

> Unlike Euclidean distance, the Haversine formula accounts for Earth's spherical geometry — essential for accurate logistics distance calculations.

---

### 3. Optimization Algorithm — Greedy Nearest Neighbor

For each truck's assigned delivery zone:

```
1. Start at Main Distribution Hub (origin)
2. Find the nearest unvisited delivery point
3. Move to that point and mark it as visited
4. Repeat Step 2–3 until all points in the zone are visited
5. Return to Main Distribution Hub (destination)
```

**Complexity:** O(n²) per cluster — computationally efficient for operational-scale deployments.

---

## 📊 Results & Fleet Performance (KPIs)

Model evaluated on **50 delivery points** across São Paulo city, producing a highly balanced workload distribution across 5 trucks:

| Fleet ID | Zone Coverage | Total Distance | Stops | Status |
|:--------:|:-------------|:--------------:|:-----:|:------:|
| 🚚 **Truck 1** | Cluster Zone 4 | 53.10 km | 10 | ✅ Optimized |
| 🚚 **Truck 2** | Cluster Zone 2 | 71.09 km | 10 | ✅ Optimized |
| 🚚 **Truck 3** | Cluster Zone 3 | 55.42 km | 10 | ✅ Optimized |
| 🚚 **Truck 4** | Cluster Zone 0 | 33.67 km | 10 | ✅ Optimized |
| 🚚 **Truck 5** | Cluster Zone 1 | 31.50 km | 10 | ✅ Optimized |
| **Total Fleet** | **Full Coverage** | **244.77 km** | **50** | ✅ **High Efficiency** |

**Key Metrics:**
```
Total Fleet Distance   : 244.77 km
Average Route Distance : 48.95 km per truck
Workload Std Deviation : ±14.8 km  (well-balanced distribution)
Delivery Points        : 50 stops fully covered
Fleet Utilization      : 100% (no unassigned stops)
```

**Figure 2:** K-Means spatial clustering (k=5) ensuring balanced workload and non-overlapping delivery zones for the fleet.
<img width="1206" height="616" alt="Screenshot 2026-05-27 201835" src="https://github.com/user-attachments/assets/a88ea863-76fa-45bb-b53f-20e6d8dea509" />

---

## 📁 Output Files

Running this project generates two publication-ready interactive HTML maps:

| File | Description |
|:-----|:------------|
| `sao_paulo_clustered_map.html` | Zone segmentation map — color-coded K-Means cluster assignment per delivery point |
| `sao_paulo_final_routes.html` | Final optimized route map — sequential delivery paths from hub to all stops per truck |

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install numpy pandas folium scikit-learn
```

| Library | Version | Purpose |
|:--------|:-------:|:--------|
| `numpy` | ≥1.21 | Numerical computation & matrix operations |
| `pandas` | ≥1.3 | Data ingestion & geospatial filtering |
| `scikit-learn` | ≥1.0 | K-Means clustering algorithm |
| `folium` | ≥0.12 | Interactive map rendering |

### Dataset

Download the Olist dataset from Kaggle:

```bash
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/ --unzip
```

> **Required file:** `olist_geolocation_dataset.csv`
> 
> Direct link: [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)



## 💡 Business Recommendations

Based on the optimization results, the following operational improvements are recommended:

1. **Adopt Zone-Based Fleet Assignment**
   Implement K-Means zone segmentation as the standard for daily fleet pre-assignment — reduces dispatcher decision time and eliminates zone overlap.

2. **Prioritize Compact Zones First**
   Trucks 4 and 5 (Zones 0 & 1, ~32 km each) should handle time-sensitive priority deliveries due to shorter route duration.

3. **Scale to Full Dataset**
   This prototype validates the methodology on 50 points. Production deployment should scale to the full São Paulo geolocation dataset (~700K records) with cluster count tuned via Elbow Method.

4. **Integrate Real-Time Traffic Data**
   Replace static Haversine distances with live traffic-weighted travel times (Google Maps API / OSRM) for dynamic re-routing capability.

5. **Extend to Capacitated VRP (CVRP)**
   Add truck payload constraints (weight/volume limits) to the current model for a full Capacitated Vehicle Routing Problem solution.

---

## 🔬 Methodology Limitations & Future Work

| Current Limitation | Proposed Enhancement |
|:-------------------|:---------------------|
| Static distance matrix | Real-time traffic API integration |
| Greedy heuristic (suboptimal) | OR-Tools / Google OR exact solver |
| No capacity constraints | Capacitated VRP (CVRP) formulation |
| 50-point sample | Full dataset deployment |
| Single depot | Multi-depot VRP extension |

---

## 📚 References

- Dantzig, G.B. & Ramser, J.H. (1959). *The Truck Dispatching Problem.* Management Science.
- Olist Brazilian E-Commerce Dataset — Kaggle (2018).
- Haversine Formula — Sinnott, R.W. (1984). *Virtues of the Haversine.* Sky and Telescope.
- Capgemini Research Institute (2019). *The Last-Mile Delivery Challenge.*

---


