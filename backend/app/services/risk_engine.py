def calculate_weather_risk(weather: dict) -> float:
    """
    Calculate weather risk from 0-25.
    """

    risk = 0

    rainfall = weather.get("rainfallMm", 0)
    wind = weather.get("windSpeedKmph", 0)
    condition = str(
        weather.get("condition", "")
    ).upper()

    # Rainfall
    if rainfall >= 100:
        risk += 15
    elif rainfall >= 50:
        risk += 10
    elif rainfall >= 20:
        risk += 5

    # Wind
    if wind >= 60:
        risk += 5
    elif wind >= 40:
        risk += 3

    # Severe weather
    if condition in [
        "HEAVY_RAIN",
        "STORM",
        "CYCLONE"
    ]:
        risk += 5

    return min(risk, 25)


def calculate_road_risk(road: dict) -> float:
    """
    Calculate road risk from 0-25.
    """

    condition = str(
        road.get("condition", "")
    ).upper()

    risk_level = str(
        road.get("riskLevel", "")
    ).upper()

    status = str(
        road.get("status", "")
    ).upper()

    risk = 0

    condition_scores = {
        "GOOD": 3,
        "FAIR": 8,
        "POOR": 17,
        "VERY_POOR": 22,
        "BLOCKED": 25,
        "CLOSED": 25
    }

    risk += condition_scores.get(
        condition,
        10
    )

    # Road risk level
    if risk_level == "CRITICAL":
        risk += 8
    elif risk_level == "HIGH":
        risk += 5
    elif risk_level == "MEDIUM":
        risk += 3

    # Road blockage
    if status in [
        "BLOCKED",
        "CLOSED"
    ]:
        risk = max(risk, 25)

    return min(risk, 25)


def calculate_disruption_risk(
    disruptions: list
) -> float:
    """
    Calculate disruption risk from 0-30.
    """

    if not disruptions:
        return 0

    risk = 0

    severity_scores = {
        "LOW": 5,
        "MEDIUM": 10,
        "HIGH": 20,
        "CRITICAL": 30
    }

    for disruption in disruptions:

        status = str(
            disruption.get(
                "status",
                ""
            )
        ).upper()

        if status != "ACTIVE":
            continue

        severity = str(
            disruption.get(
                "severity",
                "MEDIUM"
            )
        ).upper()

        current_score = severity_scores.get(
            severity,
            10
        )

        risk = max(
            risk,
            current_score
        )

    return min(risk, 30)


def calculate_gps_risk(vehicle: dict) -> float:
    """
    Calculate vehicle/GPS risk from 0-10.
    """

    speed = vehicle.get(
        "currentSpeedKmph",
        0
    )

    risk = 0

    # Unusual low speed may indicate
    # congestion or blockage
    if 0 < speed < 15:
        risk += 6

    # Excessive speed
    elif speed > 80:
        risk += 4

    return min(risk, 10)


def calculate_priority_risk(
    shipment: dict
) -> float:
    """
    Higher priority shipments receive
    higher operational risk weighting.
    """

    priority = str(
        shipment.get(
            "priority",
            "LOW"
        )
    ).upper()

    scores = {
        "LOW": 2,
        "MEDIUM": 5,
        "HIGH": 8,
        "CRITICAL": 10
    }

    return scores.get(
        priority,
        5
    )


def get_highest_active_severity(
    disruptions: list
) -> str:
    """
    Find the highest severity among
    active disruptions.
    """

    severity_rank = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    highest = "LOW"
    highest_rank = 0

    for disruption in disruptions:

        status = str(
            disruption.get(
                "status",
                ""
            )
        ).upper()

        if status != "ACTIVE":
            continue

        severity = str(
            disruption.get(
                "severity",
                "LOW"
            )
        ).upper()

        rank = severity_rank.get(
            severity,
            0
        )

        if rank > highest_rank:
            highest_rank = rank
            highest = severity

    return highest


def calculate_total_risk(
    weather: dict,
    road: dict,
    disruptions: list,
    vehicle: dict,
    shipment: dict
) -> dict:

    weather_risk = calculate_weather_risk(
        weather
    )

    road_risk = calculate_road_risk(
        road
    )

    disruption_risk = calculate_disruption_risk(
        disruptions
    )

    gps_risk = calculate_gps_risk(
        vehicle
    )

    priority_risk = calculate_priority_risk(
        shipment
    )

    total = (
        weather_risk
        + road_risk
        + disruption_risk
        + gps_risk
        + priority_risk
    )

    # ---------------------------------
    # Base risk classification
    # ---------------------------------

    if total <= 25:
        level = "LOW"

    elif total <= 50:
        level = "MEDIUM"

    elif total <= 75:
        level = "HIGH"

    else:
        level = "CRITICAL"

    # ---------------------------------
    # Context-aware risk escalation
    # ---------------------------------

    highest_severity = (
        get_highest_active_severity(
            disruptions
        )
    )

    # Critical disruption such as a
    # major landslide or completely
    # blocked road should never be
    # shown as LOW/MEDIUM.
    if highest_severity == "CRITICAL":

        level = "CRITICAL"

        # Keep the score meaningful even
        # when weather/road data is missing.
        total = max(total, 80)

    elif highest_severity == "HIGH":

        if level == "LOW":
            level = "HIGH"

        elif level == "MEDIUM":
            level = "HIGH"

        total = max(total, 60)

    elif highest_severity == "MEDIUM":

        if level == "LOW":
            level = "MEDIUM"

    return {
        "riskScore": round(total, 2),
        "riskLevel": level,
        "breakdown": {
            "weather": weather_risk,
            "road": road_risk,
            "disruption": disruption_risk,
            "gps": gps_risk,
            "priority": priority_risk
        }
    }