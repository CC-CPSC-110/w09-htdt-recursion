"""Parses stops.txt from GTFS."""
import gtfs
import math
from dataclasses import dataclass
from typing_extensions import Self

@dataclass
class Shape:
    id: str
    lat: gtfs.Latitude
    lon: gtfs.Longitude
    sequence: int
    dist_traveled: float
    next: Self
    
    def dist(self, other: Self) -> float:
        dlat = abs(self.lat - other.lat)
        dlon = abs(self.lon - other.lon)
        dist = math.sqrt(dlat ** 2 + dlon ** 2)
        return dist
    
    def dist_next(self) -> float:
        if self.next != None:
            return self.dist(self.next)
        return 0.0
    
    def dist_end(self) -> float:
        if self._next == None:
            return 0.0
        return self.dist_next() + self._next.dist_end()

# Helper function to parse a row into Shape
def parse_row_to_shape(row: str) -> Shape:
    """
    Purpose: Convert a comma-separated string row into a Stop instance.
    Example:
        parse_row_to_shape("292022,49.257645,-123.17228,1,0") 
            -> Shape(id="292022", lat=Latitude(49.257645), lon=Longitude("-123.17228"), sequence=1, dist_traveled=0)
    """
    columns = row.split(',')

    # Manually parsing each field
    id = columns[0]
    lat = gtfs.parse_latitude(columns[1])  # Use helper to parse latitude
    lon = gtfs.parse_longitude(columns[2])  # Use helper to parse longitude
    sequence = int(columns[3])
    dist_traveled = float(columns[4])

    # Return a Shape instance
    return Shape(
        id=id,
        lat=lat,
        lon=lon,
        sequence=sequence,
        dist_traveled=dist_traveled,
        next=None
    )


if __name__ == "__main__":
    with open("shapes.txt", 'r') as file:
        lines = file.readlines()
        shapes = gtfs.parse(lines[1:], parse_row_to_shape)
        print(f"There were {len(shapes)} shapes.")

        def query(**kwargs):
            """
            Purpose: Convenience function for querying shapes.
            Examples:
                query(stop_name="Westbound Davie St @ Bidwell St")
                query(stop_code="50011")
            """
            for s in gtfs.query(shapes, **kwargs):
                print(s)
        
    
    


