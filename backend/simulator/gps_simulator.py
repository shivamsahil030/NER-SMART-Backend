import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = os.getenv("GPS_API_URL", "http://127.0.0.1:8000/gps/")
SLEEP_SECONDS = float(os.getenv("GPS_SIMULATOR_SLEEP_SECONDS", "3"))


route = [
    {
        "latitude": 26.70,
        "longitude": 92.20
    },
    {
        "latitude": 26.72,
        "longitude": 92.25
    },
    {
        "latitude": 26.75,
        "longitude": 92.30
    },
    {
        "latitude": 26.78,
        "longitude": 92.36
    },
    {
        "latitude": 26.82,
        "longitude": 92.42
    },
    {
        "latitude": 26.87,
        "longitude": 92.48
    }
]


def send_gps_point(data):
    request = Request(
        API_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=10) as response:
        return response.status


def check_api_available():
    try:
        with urlopen(API_URL, timeout=3):
            return True
    except HTTPError:
        # A 405/404 still proves that the server is reachable.
        return True
    except (URLError, TimeoutError, OSError):
        return False


def main():
    if not check_api_available():
        print(
            f"Backend is unavailable at {API_URL}. "
            "Start it with: uvicorn app.main:app --reload"
        )
        return

    for index, point in enumerate(route):
        data = {
            "vehicleId": "VEH-001",
            "shipmentId": "MED-001",
            "latitude": point["latitude"],
            "longitude": point["longitude"],
            "speedKmph": 40 + index,
            "heading": 65,
        }

        try:
            status_code = send_gps_point(data)
            print(
                f"Point {index + 1}: {point['latitude']}, "
                f"{point['longitude']} -> {status_code}"
            )
        except HTTPError as error:
            print(f"Point {index + 1}: HTTP {error.code} - {error.reason}")
        except (URLError, TimeoutError, OSError) as error:
            print(f"Point {index + 1}: connection error - {error}")

        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
