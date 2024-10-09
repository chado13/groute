import heapq
import math
from dto import TripData
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
import itertools
from typing import Any
from typed import SpotData
from dto import TripData
from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, fcluster


def search(data: TripData, start: datetime, end: datetime) -> list[dict[str, Any]]:
    waypoints = [(float(each["lat"]), float(each["lng"])) for each in data.spots]
    start_geocode = (
        (float(data.arrival["lat"]), float(data.arrival["lng"]))
        if data.arrival
        else None
    )
    end_geocode = (
        (float(data.depart["lat"]), float(data.depart["lng"])) if data.depart else None
    )
    waypoints_dict = {
        (float(each["lat"]), float(each["lng"])): each for each in data.spots
    }
    waypoints_dict.update({start_geocode: data.arrival, end_geocode: data.depart})
    n_cluster = (end - start).days + 1
    points = [each for each in waypoints_dict.keys() if each]
    cluster_labels = cluster_locations(points, n_cluster)
    for key, cluster in zip(waypoints, cluster_labels):
        waypoints_dict[key]["cluster"] = int(cluster)
    optimized_clusters = []
    for label in set(cluster_labels):
        cluster = [
            waypoints[i] for i in range(len(waypoints)) if cluster_labels[i] == label
        ]
        print(cluster)
        if cluster:
            optimized_clusters.append(optimize_cluster_path(cluster))
    final_path = optimize_full_path(start_geocode, end_geocode, optimized_clusters)

    cluster_groups = {}
    for lat_lng in final_path:
        data = waypoints_dict[lat_lng]
        cluster = data.get("cluster")
        if cluster is not None:
            if cluster not in cluster_groups:
                cluster_groups[cluster] = []
            cluster_groups[cluster].append(lat_lng)
    res = [
        {
            "name": start.strftime("%m.%d"),
            "id": 1,
            "type": "spliter",
            "day": None,
            "order": None,
            "lat": None,
            "lng": None,
            "address": None,
            "category": None,
            "cluster": None,
        }
    ]
    prev_cluster = None
    day = 1
    id = 0
    s_id = 1
    order = 1
    processed_points = set()
    for i, lat_lng in enumerate(final_path):
        if lat_lng != start_geocode or lat_lng != end_geocode:
            if lat_lng in processed_points:
                continue
        data = waypoints_dict[lat_lng].copy()
        cluster = data.get("cluster")
        if cluster is not None and cluster in cluster_groups.keys():
            for point in cluster_groups[cluster]:
                point_data = waypoints_dict[point].copy()
                point_data["order"] = order
                point_data["type"] = "place"
                point_data["id"] = id
                point_data["day"] = day
                res.append(point_data)
                processed_points.add(point)
                id += 1
                order += 1
            # 다음 날짜로 이동

            dt = start + timedelta(days=day - 1)
            if dt < end:
                day += 1
                s_id += 1
                res.append(
                    {
                        "name": dt.strftime("%m.%d"),
                        "id": s_id,
                        "type": "spliter",
                        "day": day,
                        "order": None,
                        "lat": None,
                        "lng": None,
                        "address": None,
                        "category": None,
                        "cluster": None,
                    }
                )
        else:
            # 클러스터가 없는 지점 처리(시작점, 종료점)
            data["order"] = i + 1
            data["type"] = "place"
            data["id"] = id
            data["day"] = day
            res.append(data)
            processed_points.add(lat_lng)
            id += 1
            order += 1
    return res


# 군집화
def cluster_locations(
    waypoints: list[tuple[int, int]], n_clusters: int | None
) -> list[int]:
    n_clusters = n_clusters if n_clusters else 1
    scaler = StandardScaler()
    waypoints_scaled = scaler.fit_transform(waypoints)
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(waypoints_scaled)
    return kmeans.labels_
    # distance_matrix = haversine_distance_matrix(waypoints)
    # Z = linkage(distance_matrix, method='ward')  # 'ward' 메소드를 사용한 클러스터링
    # return fcluster(Z, n_clusters, criterion='maxclust')


def haversine_distance_matrix(waypoints):
    return squareform(pdist(waypoints, metric=haversine))


def haversine(coord1, coord2):
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    R = 6371.0  # 지구 반지름 (km)
    return R * c


# 군집 내 최적경로 계산
def optimize_cluster_path(cluster: np.ndarray) -> list[tuple[float, float]]:
    distances = squareform(pdist(cluster, metric=haversine_wrapper))
    n = len(cluster)
    best_path = list(range(n))
    best_distance = sum(distances[i][i + 1] for i in range(n - 1))

    for path in itertools.permutations(range(n)):
        distance = sum(distances[path[i]][path[i + 1]] for i in range(n - 1))
        if distance < best_distance:
            best_path = path
            best_distance = distance

    return [cluster[i] for i in best_path]


# 전체 경로 최적화
def optimize_full_path(start, end, clusters):
    all_points = [point for cluster in clusters for point in cluster]
    if start:
        all_points = [start] + all_points
    if end:
        all_points = all_points + [end]
    distances = squareform(pdist(all_points, metric=haversine_wrapper))
    n = len(all_points)

    # 동적 프로그래밍을 사용한 최적 경로 찾기
    dp = [[float("inf")] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1, 1 << n):
        for i in range(n):
            if mask & (1 << i):
                for j in range(n):
                    if i != j and mask & (1 << j):
                        dp[mask][i] = min(
                            dp[mask][i], dp[mask ^ (1 << i)][j] + distances[j][i]
                        )

    # 최적 경로 재구성
    mask = (1 << n) - 1
    last = n - 1
    path = [last]
    while mask != 1:
        nxt = min(
            range(n),
            key=lambda x: (
                dp[mask][x] + distances[x][last]
                if x != last and mask & (1 << x)
                else float("inf")
            ),
        )
        path.append(nxt)
        mask ^= 1 << last
        last = nxt

    return [all_points[i] for i in reversed(path)]


def haversine_vector(points):
    n = points.shape[0]
    distances = np.zeros((n * (n - 1)) // 2)
    k = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            distances[k] = haversine(
                points[i, 0], points[i, 1], points[j, 0], points[j, 1]
            )
            k += 1
    return distances


def haversine(coord1, coord2):
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 지구 반지름 (km)
    R = 6371.0
    distance = R * c
    return distance


def haversine_wrapper(u, v):
    return haversine(u, v)
