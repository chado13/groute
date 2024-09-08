import math
from typing import List, Tuple


# 위도와 경도를 사용하여 두 지점 간의 거리를 계산하는 함수
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371  # 지구의 반경 (km)

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    return R * c


# 최근접 이웃 알고리즘
def nearest_neighbor(points: List[Tuple[float, float]]) -> List[int]:
    n = len(points)
    unvisited = set(range(1, n))
    route = [0]

    while unvisited:
        last = route[-1]
        next_point = min(
            unvisited,
            key=lambda x: haversine_distance(
                points[last][0], points[last][1], points[x][0], points[x][1]
            ),
        )
        route.append(next_point)
        unvisited.remove(next_point)

    return route


# 2-opt 최적화
def two_opt(route: List[int], points: List[Tuple[float, float]]) -> List[int]:
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                new_route = route[:]
                new_route[i:j] = route[j - 1 : i - 1 : -1]
                if route_distance(new_route, points) < route_distance(best, points):
                    best = new_route
                    improved = True
        route = best
    return best


# 전체 경로의 거리를 계산하는 함수
def route_distance(route: List[int], points: List[Tuple[float, float]]) -> float:
    return sum(
        haversine_distance(
            points[route[i]][0],
            points[route[i]][1],
            points[route[i + 1]][0],
            points[route[i + 1]][1],
        )
        for i in range(len(route) - 1)
    )


# 메인 함수
def optimize_route(points: List[Tuple[float, float]]) -> List[int]:
    initial_route = nearest_neighbor(points)
    optimized_route = two_opt(initial_route, points)
    return optimized_route


# 사용 예시
if __name__ == "__main__":
    # 예시 좌표 (위도, 경도)
    locations = [
        (37.7929448142, 128.9145027351),  # 툇마루
        (37.7912255723, 128.9146972153),  # 동화가든
        (37.7948530151, 128.9190439335),  # 강문해변
        (37.7917838566, 128.9154887933),  # 순두부젤라또
    ]

    best_route = optimize_route(locations)

    print("최적화된 경로:")
    for i in best_route:
        print(f"위치 {i}: ({locations[i][0]}, {locations[i][1]})")

    print(f"총 거리: {route_distance(best_route, locations):.2f} km")
