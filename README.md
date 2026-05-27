# Geospatial Logistics & Route Optimization: São Paulo E-Commerce (Olist)

Proyek ini mengimplementasikan solusi **Data Science** dan **Operations Research (OR)** end-to-end untuk mengoptimalkan operasional distribusi logistik *last-mile* di kota São Paulo, Brazil. Menggunakan data riil dari **Olist E-Commerce Dataset**, proyek ini memecahkan tantangan alokasi armada truk dan minimasi jarak tempuh melalui pendekatan *Machine Learning* dan optimasi heuristik.

## 📌 Ringkasan Solusi
Sistem optimasi rute ini bekerja melalui dua tahapan utama:
1. **Regional Clustering (K-Means):** Mengelompokkan 50 titik pengiriman acak ke dalam 5 zona wilayah operasional yang seimbang berdasarkan kedekatan koordinat geografis (mensimulasikan pembagian kerja untuk 5 armada truk).
2. **Vehicle Routing Problem (VRP) Optimization:** Menentukan urutan kunjungan rute terpendek untuk setiap truk di dalam zona masing-masing menggunakan pendekatan **Greedy Nearest Neighbor Heuristic** guna meminimalkan total jarak tempuh (*objective function*).

---

## 🛠️ Arsitektur Sistem & Metodologi

### 1. Formulasi Matematis (Objective Function)
Tujuan utama dari model optimasi ini adalah meminimalkan total jarak geografis yang ditempuh oleh seluruh armada kendaraan dari Gudang Utama (*Main Distribution Hub*), mengunjungi semua titik konsumen di zonanya, dan kembali ke Gudang Utama.

$$\min Z = \sum_{k=1}^{K} \sum_{i=0}^{N} \sum_{j=0}^{N} d_{ij} x_{ijk}$$

**Batasan Model (Constraints):**
* Setiap titik pengiriman konsumen $i$ wajib dikunjungi tepat satu kali oleh satu armada truk tertentu.
* Setiap rute perjalanan armada $k$ harus dimulai dari Gudang Utama ($i=0$) dan diakhiri kembali di Gudang Utama ($j=0$).
* Jarak antar koordinat bola bumi ($d_{ij}$) dihitung secara presisi menggunakan **Formula Haversine**:

$$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)}\right)$$

*Dimana:*
* $\phi$: Lintang (*Latitude*) dalam radian.
* $\lambda$: Bujur (*Longitude*) dalam radian.
* $R$: Jari-jari bumi (6.371 Km).

### 2. Alur Pipa Data (Data Pipeline)
* **Data Ingestion & Cleaning:** Memfilter data spasial khusus wilayah São Paulo dari berkas `olist_geolocation_dataset.csv`, mereduksi duplikasi koordinat, dan mengekstrak sampel 50 titik distribusi aktif.
* **Spatial Segmenting:** Menggunakan algoritma *Unsupervised Learning* K-Means untuk membagi titik koordinat menjadi klaster wilayah yang optimal secara spasial.
* **Heuristic Routing:** Menerapkan algoritma *Greedy Nearest Neighbor* untuk menyusun lintasan urutan kunjungan guna menghindari rute bersilang yang tidak efisien.
* **Interactive Cartography:** Memetakan seluruh jaringan rute menggunakan *Folium PolyLine* menjadi visualisasi peta interaktif berbasis web.

---

## 📊 Hasil Analisis & Kinerja Armada (Key Performance Indicators)

Evaluasi model pada 50 titik pengiriman di kota São Paulo menghasilkan pembagian beban kerja operasional yang sangat efisien bagi 5 armada truk:

| ID Armada | Cakupan Zona Wilayah | Total Jarak Tempuh (Km) | Status Operasional |
| :--- | :--- | :--- | :--- |
| 🚚 **Truk 1** | Cluster Zona 4 | 53.10 km | Teroptimasi |
| 🚚 **Truk 2** | Cluster Zona 2 | 71.09 km | Teroptimasi |
| 🚚 **Truk 3** | Cluster Zona 3 | 55.42 km | Teroptimasi |
| 🚚 **Truk 4** | Cluster Zona 0 | 33.67 km | Teroptimasi |
| 🚚 **Truk 5** | Cluster Zona 1 | 31.50 km | Teroptimasi |
| **Total Fleet** | **Seluruh Wilayah** | **244.77 km** | **Efisiensi Tinggi** |

---

## 📁 Struktur Berkas Hasil Output

Eksekusi proyek ini memproduksi dua berkas peta interaktif dalam format HTML yang siap dipublikasikan:
* `sao_paulo_clustered_map.html`: Peta visualisasi segmentasi wilayah kerja 5 armada truk berdasarkan output K-Means.
* `sao_paulo_final_routes.html`: Peta rute perjalanan final yang menghubungkan hub distribusi ke seluruh titik pengiriman konsumen secara berurutan tanpa rute bersilang.

---

## 🚀 Panduan Menjalankan Kode

### Prasyarat Pustaka (Dependencies)
Pastikan lingkungan Python Anda telah terinstal beberapa pustaka berikut:
```bash
pip install numpy pandas folium scikit-learn
