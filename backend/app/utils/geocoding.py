"""Geocoding utility — convert location text to coordinates."""

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


async def geocode_location(
    location_text: str,
    api_key: Optional[str] = None,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Convert a location description to lat/lng coordinates
    using Google Maps Geocoding API.
    Returns (latitude, longitude) or (None, None) on failure.
    """
    if not location_text:
        return None, None

    try:
        import httpx
        from app.config import settings

        key = api_key or settings.GOOGLE_MAPS_API_KEY
        if not key:
            logger.warning("No Google Maps API key configured")
            return None, None

        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": location_text, "key": key}

        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=10)
            data = resp.json()

        if data.get("results"):
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
        return None, None

    except Exception as e:
        logger.error(f"Geocoding failed for '{location_text}': {e}")
        return None, None


# Default ward coordinates for demo (Delhi-based)
WARD_COORDINATES: dict[int, Tuple[float, float]] = {
    1: (28.6139, 77.2090),
    2: (28.6280, 77.2185),
    3: (28.6353, 77.2249),
    4: (28.6508, 77.2335),
    5: (28.6445, 77.2088),
    6: (28.6100, 77.2300),
    7: (28.6200, 77.2400),
    8: (28.6350, 77.2100),
    9: (28.6412, 77.2500),
    10: (28.6050, 77.2150),
    11: (28.6550, 77.2200),
    12: (28.6180, 77.2350),
    13: (28.6320, 77.2050),
    14: (28.6470, 77.2420),
    15: (28.6250, 77.2280),
}


def get_ward_coords(ward_id: int) -> Tuple[Optional[float], Optional[float]]:
    """Return default coordinates for a ward (demo data)."""
    return WARD_COORDINATES.get(ward_id, (None, None))
