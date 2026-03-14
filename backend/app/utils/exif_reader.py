"""EXIF data reader — extract GPS, timestamp, camera info from images."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def extract_exif_data(image_path: str) -> dict:
    """Extract GPS, timestamp, and camera info from image EXIF data."""
    result = {
        "gps_latitude": None,
        "gps_longitude": None,
        "datetime": None,
        "make": None,
        "model": None,
        "software": None,
    }

    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS

        img = Image.open(image_path)
        exif_data = img._getexif()

        if not exif_data:
            return result

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)

            if tag == "DateTime":
                result["datetime"] = value
            elif tag == "Make":
                result["make"] = value
            elif tag == "Model":
                result["model"] = value
            elif tag == "Software":
                result["software"] = value
            elif tag == "GPSInfo":
                gps_data = {}
                for gps_tag_id, gps_value in value.items():
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_data[gps_tag] = gps_value

                if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                    result["gps_latitude"] = _convert_to_degrees(
                        gps_data["GPSLatitude"],
                        gps_data.get("GPSLatitudeRef", "N"),
                    )
                    result["gps_longitude"] = _convert_to_degrees(
                        gps_data["GPSLongitude"],
                        gps_data.get("GPSLongitudeRef", "E"),
                    )
    except Exception as e:
        logger.warning(f"EXIF extraction error: {e}")

    return result


def _convert_to_degrees(value, ref: str) -> float:
    """Convert GPS coordinates to decimal degrees."""
    d, m, s = value
    degrees = float(d) + float(m) / 60 + float(s) / 3600
    if ref in ("S", "W"):
        degrees = -degrees
    return degrees
