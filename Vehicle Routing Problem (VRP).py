# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "folium==0.20.0",
#     "marimo>=0.23.8",
#     "numpy==2.4.4",
#     "pandas==3.0.2",
#     "scikit-learn==1.8.0",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell
def _():
    import pandas as pd
    import folium
    from folium.plugins import MarkerCluster
    import numpy as np
    import warnings
    warnings.filterwarnings('ignore')

    # ==========================================
    # 1. DATA INGESTION (OLIST KAGGLE DATASET)
    # ==========================================
    print("Loading Olist Geolocation Dataset...")
    # Sesuaikan path ini jika folder data Anda berbeda

    file_path = 'olist_geolocation_dataset.csv'

    try:
        df_geo = pd.read_csv(file_path)
        print("Dataset successfully loaded!")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the path.")
        exit()

    # Filter data hanya untuk kota São Paulo agar simulasi rute realistis
    df_sp = df_geo[df_geo['geolocation_city'] == 'sao paulo']

    # Hapus koordinat duplikat (banyak pelanggan di kode pos yang sama)
    df_sp = df_sp.drop_duplicates(subset=['geolocation_lat', 'geolocation_lng'])

    # Ambil sampel 50 titik pengiriman acak untuk optimasi VRP
    df_sample = df_sp.sample(n=50, random_state=42).reset_index(drop=True)

    # Tambahkan simulasi volume permintaan (karena dataset asli hanya berisi koordinat)
    df_sample['demand'] = np.random.randint(10, 150, size=len(df_sample))

    print("\nSample Delivery Points in São Paulo:")
    print(df_sample[['geolocation_lat', 'geolocation_lng', 'demand']].head())

    # ==========================================
    # 2. INTERACTIVE MAP VISUALIZATION (FOLIUM)
    # ==========================================
    # Tetapkan Distribution Hub di tengah-tengah semua titik pengiriman
    HUB_LATITUDE = df_sample['geolocation_lat'].mean()
    HUB_LONGITUDE = df_sample['geolocation_lng'].mean()

    # Inisialisasi peta dasar dengan fokus di São Paulo
    logistics_map = folium.Map(location=[HUB_LATITUDE, HUB_LONGITUDE], zoom_start=12, tiles='CartoDB positron')

    # Tambahkan penanda untuk Distribution Hub (Gudang Utama)
    folium.Marker(
        location=[HUB_LATITUDE, HUB_LONGITUDE],
        popup="<b>MAIN DISTRIBUTION HUB (São Paulo)</b>",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(logistics_map)

    # Buat Marker Cluster agar peta terlihat rapi
    marker_cluster = MarkerCluster().add_to(logistics_map)

    # Tambahkan 50 titik pengiriman (toko/pelanggan) ke dalam peta
    for index, row in df_sample.iterrows():
        folium.Marker(
            location=[row['geolocation_lat'], row['geolocation_lng']],
            popup=f"<b>Delivery Node {index+1}</b><br>Demand: {row['demand']} units",
            icon=folium.Icon(color='blue', icon='shopping-cart')
        ).add_to(marker_cluster)

    # Simpan peta interaktif sebagai file HTML
    map_filename = "sao_paulo_logistics_map.html"
    logistics_map.save(map_filename)
    print(f"\nInteractive map successfully generated and saved as: {map_filename}")
    return HUB_LATITUDE, HUB_LONGITUDE, df_sample, folium, np


@app.cell
def _(df_sample):
    def _():
        import folium
        from sklearn.cluster import KMeans

        # ==========================================
        # 3. K-MEANS GEOSPATIAL CLUSTERING
        # ==========================================
        print("Applying K-Means Clustering to delivery points...")

        # Assume we have 5 delivery trucks, so we divide the points into 5 zones
        NUM_TRUCKS = 5

        # Extract the latitude and longitude as features for the Machine Learning model
        X_coords = df_sample[['geolocation_lat', 'geolocation_lng']].values

        # Initialize and fit the K-Means algorithm
        kmeans = KMeans(n_clusters=NUM_TRUCKS, random_state=42, n_init=10)
        df_sample['cluster'] = kmeans.fit_predict(X_coords)

        print("\nCluster assignment completed. Sample data with clusters:")
        print(df_sample[['geolocation_lat', 'geolocation_lng', 'demand', 'cluster']].head())

        # ==========================================
        # 4. VISUALIZING THE CLUSTERED ZONES
        # ==========================================
        # Re-initialize the map centered at the hub
        HUB_LATITUDE = df_sample['geolocation_lat'].mean()
        HUB_LONGITUDE = df_sample['geolocation_lng'].mean()

        clustered_map = folium.Map(location=[HUB_LATITUDE, HUB_LONGITUDE], zoom_start=12, tiles='CartoDB positron')

        # Add the Main Distribution Hub marker
        folium.Marker(
            location=[HUB_LATITUDE, HUB_LONGITUDE],
            popup="<b>MAIN DISTRIBUTION HUB</b>",
            icon=folium.Icon(color='red', icon='home', prefix='fa') # 'fa' for FontAwesome icons
        ).add_to(clustered_map)

        # Define distinct colors for our 5 delivery trucks (clusters)
        cluster_colors = ['blue', 'green', 'purple', 'orange', 'darkblue']

        # Plot each delivery point, colored by its assigned truck/zone
        for index, row in df_sample.iterrows():
            cluster_id = int(row['cluster'])

            folium.Marker(
                location=[row['geolocation_lat'], row['geolocation_lng']],
                popup=f"<b>Node {index+1}</b><br>Demand: {row['demand']}<br>Truck Zone: {cluster_id}",
                icon=folium.Icon(color=cluster_colors[cluster_id], icon='shopping-cart')
            ).add_to(clustered_map)

        # Save the clustered map
        cluster_map_filename = "sao_paulo_clustered_map.html"
        clustered_map.save(cluster_map_filename)
        return print(f"\nClustered map successfully saved as: {cluster_map_filename}")


    _()
    return


@app.cell
def _(HUB_LATITUDE, HUB_LONGITUDE, df_sample, folium, np):
    # ==========================================
    # 5. GEOSPATIAL DISTANCE CALCULATION
    # ==========================================
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Menghitung jarak lingkaran besar (great-circle) antara dua titik 
        di permukaan bumi menggunakan formula Haversine (dalam Kilometer).
        """
        R = 6371.0 # Jari-jari bumi dalam kilometer

        # Konversi derajat ke radian
        lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(np.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))

        return R * c

    # ==========================================
    # 6. ROUTE OPTIMIZATION (NEAREST NEIGHBOR)
    # ==========================================
    print("Optimizing delivery routes for each truck zone...")

    # Menambahkan definisi di sini agar terhindar dari NameError
    NUM_TRUCKS = 5

    # Inisialisasi peta final
    final_route_map = folium.Map(location=[HUB_LATITUDE, HUB_LONGITUDE], zoom_start=12, tiles='CartoDB positron')

    # Tambahkan Gudang Utama
    folium.Marker(
        location=[HUB_LATITUDE, HUB_LONGITUDE],
        popup="<b>MAIN DISTRIBUTION HUB</b>",
        icon=folium.Icon(color='red', icon='home', prefix='fa')
    ).add_to(final_route_map)

    cluster_colors_vrp = ['blue', 'green', 'purple', 'orange', 'darkblue']
    total_fleet_distance = 0

    # Iterasi untuk mencari rute terbaik di Masing-Masing Zona (Truk)
    for cluster_id in range(NUM_TRUCKS):
        # Ambil semua titik yang masuk ke zona (cluster) ini
        cluster_nodes = df_sample[df_sample['cluster'] == cluster_id].copy()
        unvisited_nodes = cluster_nodes[['geolocation_lat', 'geolocation_lng']].values.tolist()

        current_location = [HUB_LATITUDE, HUB_LONGITUDE]
        route_coordinates = [current_location]
        zone_distance = 0

        # Algoritma Nearest Neighbor (Cari titik terdekat yang belum dikunjungi)
        while unvisited_nodes:
            nearest_node = None
            min_distance = float('inf')

            for node in unvisited_nodes:
                dist = haversine_distance(current_location[0], current_location[1], node[0], node[1])
                if dist < min_distance:
                    min_distance = dist
                    nearest_node = node

            # Pindah ke titik terdekat tersebut
            route_coordinates.append(nearest_node)
            zone_distance += min_distance
            unvisited_nodes.remove(nearest_node)
            current_location = nearest_node

        # Perjalanan pulang kembali ke Gudang (Hub)
        return_dist = haversine_distance(current_location[0], current_location[1], HUB_LATITUDE, HUB_LONGITUDE)
        zone_distance += return_dist
        route_coordinates.append([HUB_LATITUDE, HUB_LONGITUDE])

        total_fleet_distance += zone_distance
        print(f"Truck {cluster_id + 1} Route Distance: {zone_distance:.2f} km")

        # Gambarkan garis rute di atas peta
        folium.PolyLine(
            route_coordinates, 
            color=cluster_colors_vrp[cluster_id], 
            weight=3, 
            opacity=0.8,
            tooltip=f"Route Truck {cluster_id + 1}"
        ).add_to(final_route_map)

        # Tambahkan marker kecil untuk toko-tokonya
        for node in route_coordinates[1:-1]:
            folium.CircleMarker(
                location=node, 
                radius=5, 
                color=cluster_colors_vrp[cluster_id], 
                fill=True,
                fill_opacity=0.9
            ).add_to(final_route_map)

    print(f"\nTotal Fleet Distance for all deliveries: {total_fleet_distance:.2f} km")

    # Simpan peta rute final
    final_map_filename = "sao_paulo_final_routes.html"
    final_route_map.save(final_map_filename)
    print(f"Final route map successfully saved as: {final_map_filename}")
    return


if __name__ == "__main__":
    app.run()
