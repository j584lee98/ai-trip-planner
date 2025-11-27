from typing import List


async def search_flights(origin: str, destination: str, date: str) -> List[dict]:
    # TODO: integrate a real flights API
    return [
        {"carrier": "Demo Air", "origin": origin, "destination": destination, "date": date, "price": 199.0}
    ]


async def search_hotels(city: str, check_in: str, check_out: str) -> List[dict]:
    # TODO: integrate a real hotels API
    return [
        {"name": "Demo Hotel", "city": city, "check_in": check_in, "check_out": check_out, "price": 129.0}
    ]
