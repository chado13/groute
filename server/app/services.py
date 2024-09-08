import heapq
import math
from app.dto import TripData
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform
import itertools
from typing import Any
from app.typed import SpotData
from app.dto import TripData
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

def search(data: TripData) -> list[dict[str,Any]]:
    start_geocode = (float(data.arrival["lat"]), float(data.arrival["lng"]))
    end_geocode = (float(data.depart["lat"]), float(data.depart["lng"]))
    waypoints_dict = {(float(each["lat"]), float(each["lng"])):each for each in data.spots}
    waypoints_dict.update({start_geocode:data.arrival, end_geocode:data.depart})
    waypoints = [(float(each["lat"]), float(each["lng"])) for each in data.spots]
    start = datetime.strptime(data.schedule[0], '%Y-%m-%dT%H:%M:%S.%fZ')
    end = datetime.strptime(data.schedule[-1], '%Y-%m-%dT%H:%M:%S.%fZ')
    n_cluster = (end - start).days + 1
    cluster_labels = cluster_locations(waypoints, n_cluster)
    optimized_clusters = []
    for label in set(cluster_labels):
        cluster = [waypoints[i] for i in range(len(waypoints)) if cluster_labels[i] == label]
        optimized_clusters.append(optimize_cluster_path(cluster))
    final_path = optimize_full_path(start_geocode, end_geocode, optimized_clusters)
    res = []
    for i, lat_lng in enumerate(final_path):
        data = waypoints_dict[lat_lng]
        data["order"] = i + 1
        res.append(data)
    return res


#군집화
def cluster_locations(waypoints:list[tuple[int,int]], n_clusters: int | None) -> list[int]:
    n_clusters = n_clusters if n_clusters else 3
    kmeans = KMeans(n_clusters=max(n_clusters, 3))
    kmeans.fit(waypoints)
    return kmeans.labels_

#군집 내 최적경로 계산
def optimize_cluster_path(cluster: np.ndarray) -> list[tuple[float, float]]:
    distances = squareform(pdist(cluster, metric=haversine_wrapper))
    n = len(cluster)
    best_path = list(range(n))
    best_distance = sum(distances[i][i+1] for i in range(n-1))
    
    for path in itertools.permutations(range(n)):
        distance = sum(distances[path[i]][path[i+1]] for i in range(n-1))
        if distance < best_distance:
            best_path = path
            best_distance = distance
    
    return [cluster[i] for i in best_path]

# 전체 경로 최적화
def optimize_full_path(start, end, clusters):
    all_points = [start] + [point for cluster in clusters for point in cluster] + [end]
    distances = squareform(pdist(all_points, metric=haversine_wrapper))
    n = len(all_points)
    
    # 동적 프로그래밍을 사용한 최적 경로 찾기
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0
    
    for mask in range(1, 1 << n):
        for i in range(n):
            if mask & (1 << i):
                for j in range(n):
                    if i != j and mask & (1 << j):
                        dp[mask][i] = min(dp[mask][i], dp[mask ^ (1 << i)][j] + distances[j][i])
    
    # 최적 경로 재구성
    mask = (1 << n) - 1
    last = n - 1
    path = [last]
    while mask != 1:
        nxt = min(range(n), key=lambda x: dp[mask][x] + distances[x][last] if x != last and mask & (1 << x) else float('inf'))
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
            distances[k] = haversine(points[i, 0], points[i, 1], points[j, 0], points[j, 1])
            k += 1
    return distances

def haversine(coord1, coord2):
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 지구 반지름 (km)
    R = 6371.0
    distance = R * c
    return distance


def haversine_wrapper(u, v):
    return haversine(u, v)