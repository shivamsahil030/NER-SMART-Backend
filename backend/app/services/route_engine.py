def calculate_route_score(
    distance_km: float,
    estimated_time_minutes: float,
    risk_score: float
) -> float:
    """
    Lower score = better route.

    Risk is intentionally weighted heavily because
    NER-LOGIX prioritizes safe logistics over shortest distance.
    """

    time_score = estimated_time_minutes / 10
    distance_score = distance_km / 10
    risk_weight = risk_score * 2

    return round(
        distance_score + time_score + risk_weight,
        2
    )


def recommend_route(routes: list[dict]) -> dict:
    """
    Select the safest practical route from candidates.
    """

    if not routes:
        return {
            "status": "NO_ROUTE",
            "message": "No candidate routes available"
        }

    evaluated_routes = []

    for route in routes:

        score = calculate_route_score(
            distance_km=route["distanceKm"],
            estimated_time_minutes=route["estimatedTimeMinutes"],
            risk_score=route["riskScore"]
        )

        evaluated_routes.append({
            **route,
            "optimizationScore": score
        })

    recommended = min(
        evaluated_routes,
        key=lambda route: route["optimizationScore"]
    )

    return {
        "status": "ROUTE_FOUND",
        "recommendedRoute": recommended,
        "alternatives": evaluated_routes
    }