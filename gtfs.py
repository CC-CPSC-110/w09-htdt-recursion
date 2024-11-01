import re
from enum import Enum
from typing import List, Any
from typing_extensions import Self
from dataclasses import dataclass

@dataclass
class Range:
    """Class to validate if a given value is within a specified range."""       

    def validate(self, value:     float | int,
                       min_value: float | int,
                       max_value: float | int) -> float | int:
        """
        Purpose: Validates if the value is within the specified min and max range.
        Example:
            validate(10,0,10) -> True
            validate(10,0, 9) -> False
        """
        if not (min_value <= value <= max_value):
            raise ValueError(
                f"Value {value} is out of range [{min_value}, {max_value}]"
            )
        return value


@dataclass
class Latitude(Range):
    """Class to validate and normalize the latitude value."""
    lat: float

    def __init__(self, lat: float) -> None:
        self.lat = self.normalize(lat)

    def normalize(self, lat: float) -> float:
        """Normalize latitude with reflection across poles."""
        if lat > 90:
            return 90 - (lat - 90)
        elif lat < -90:
            return -90 - (lat + 90)
        return lat

    def __add__(self, other: Self) -> Self:
        return Latitude(self.normalize(self.lat + other.lat))

    def __sub__(self, other: Self) -> Self:
        return Latitude(self.normalize(self.lat - other.lat))

    def __abs__(self) -> float:
        """Returns the absolute value of the latitude."""
        return abs(self.lat)


@dataclass
class Longitude(Range):
    """Class to validate the longitude value."""
    lon: float

    def __init__(self, lon: float) -> None:
        self.lon = self.validate(lon, -180.0, 180.0)

    def __add__(self, other: Self) -> Self:
        new_lon = (self.lon + other.lon + 180) % 360 - 180  # Wraps around [-180, 180]
        return Longitude(new_lon)

    def __sub__(self, other: Self) -> Self:
        new_lon = (self.lon - other.lon + 180) % 360 - 180  # Wraps around [-180, 180]
        return Longitude(new_lon)
    
    def __abs__(self) -> float:
        """Returns the absolute value of the longitude."""
        return abs(self.lon)
    

@dataclass
class LocationType(Enum):
    """Enum to define different location types for a stop."""
    STOP = 0       # Standard stop
    STATION = 1    # Station
    ENTRANCE = 2   # Entrance/exit
    GENERIC = 3    # Generic node
    BOARDING = 4   # Boarding area


@dataclass
class WheelChairBoarding(Enum):
    INHERIT = 0        # Parentless means none, otherwise inherit
    ACCESSIBLE = 1     # Some accessible path or vehicles
    INACCESSIBLE = 2   # No accessible paths or vehicles



@dataclass
class URL:
    """Class to validate and store a URL."""
    def __init__(self, url: str) -> None:
        """Initialize the URL after validating it."""
        if self.validate(url):
            self.url = url
            
    def validate(self, url: str) -> bool:
        """
        Purpose: Validates if the given string is a valid URL.
        Example:
            validate("https://hello.com") -> True
            validate("hts://hello.com") -> False
        """
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # Protocol (http, https, ftp)
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain name
            r'localhost|'  # Localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
            r'(?::\d+)?'  # Optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
        return re.match(regex, url) is not None  # Returns True if the URL is valid, otherwise False




# Helper function to parse latitude
def parse_latitude(value: str) -> Latitude:
    """
    Purpose: Convert a string to a validated Latitude instance.
    Example:
        parse_latitude("49.286458") -> Latitude(49.286458)
    """
    return Latitude(float(value))

# Helper function to parse longitude
def parse_longitude(value: str) -> Longitude:
    """
    Purpose: Convert a string to a validated Longitude instance.
    Example:
        parse_longitude("-123.140424") -> Longitude(-123.140424)
    """
    return Longitude(float(value))

# Helper function to parse the URL
def parse_url(value: str) -> URL | None:
    """
    Purpose: Convert a string to a validated URL
    instance if not empty, or None if empty.
    Examples:
        parse_url("https://www.example.com") -> URL("https://www.example.com")
        parse_url("") -> None
    """
    return URL(value) if value else None

# Helper function to parse LocationType
def parse_location_type(value: str) -> LocationType:
    """
    Purpose: Convert a string to a LocationType enum.
    Example:
        parse_location_type("0") -> LocationType.STOP
    """
    return LocationType(int(value))

# Helper function to parse WheelChairBoarding
def parse_wheelchair_boarding(value: str) -> WheelChairBoarding:
    """
    Purpose: Convert a string to a WheelChairBoarding enum.
    Example:
        parse_wheelchair_boarding("1") -> WheelChairBoarding.ACCESSIBLE
    """
    return WheelChairBoarding(int(value))
    

def parse(rows: List[str], parser: Any) -> Any:
    return [parser(row) for row in rows]


def query(items: list[Any], **filters) -> list[Any]:
    """
    Purpose: Query the list of items based on filters such as stop_name, stop_code, zone_id, etc.
    Example:
        query(stops, stop_name="Westbound Davie St @ Bidwell St") -> list of matching Stop instances
    Args:
        stops: List of Stop instances.
        **filters: Keyword arguments for filtering the stops (e.g., stop_name="Westbound Davie St @ Bidwell St").
    Returns:
        List of Stop instances that match all the provided filters.
    """
    results = items

    for attr, value in filters.items():
        results = [item for item in results if getattr(item, attr) == value]
    
    return results