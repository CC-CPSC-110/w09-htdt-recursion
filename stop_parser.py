"""Parses stops.txt from GTFS."""
import gtfs
from dataclasses import dataclass

@dataclass
class Stop:
    stop_id: str 
    stop_code: str
    stop_name: str
    stop_desc: str | None
    stop_lat: gtfs.Latitude
    stop_lon: gtfs.Longitude
    zone_id: str
    stop_url: gtfs.URL | None
    location_type: gtfs.LocationType
    parent_station: str # Foreign
    wheelchair_boarding: gtfs.WheelChairBoarding
    
    def __str__(self) -> str:
        """
        Purpose: Pretty-print the Stop instance in a readable format.
        
        Example:
            Stop Name: Westbound Davie St @ Bidwell St
            Stop Code: 50001
            Latitude: 49.286458, Longitude: -123.140424
            Zone ID: BUS ZN
            Location Type: STOP
            Wheelchair Boarding: ACCESSIBLE
        """
        return (f"Stop Name: {self.stop_name}\n"
                f"Stop Code: {self.stop_code}\n"
                f"Stop Description: {self.stop_desc or 'N/A'}\n"
                f"Latitude: {self.stop_lat.lat}, Longitude: {self.stop_lon.lon}\n"
                f"Zone ID: {self.zone_id}\n"
                f"URL: {self.stop_url.url if self.stop_url else 'N/A'}\n"
                f"Location Type: {self.location_type.name}\n"
                f"Wheelchair Boarding: {self.wheelchair_boarding.name}\n")


# Helper function to parse a row into Stop
def parse_row_to_stop(row: str) -> Stop:
    """
    Purpose: Convert a comma-separated string row into a Stop instance.
    Example:
        parse_row_to_stop("1,50001,Westbound Davie St @ Bidwell St,,49.286458,-123.140424,BUS ZN,,0,,1") 
            -> Stop(stop_id="1", stop_code="50001", stop_name="Westbound Davie St @ Bidwell St", ...)
    """
    columns = row.split(',')

    # Manually parsing each field
    stop_id = columns[0]
    stop_code = columns[1]
    stop_name = columns[2]
    stop_desc = columns[3] if columns[3] else None
    stop_lat = gtfs.parse_latitude(columns[4])  # Use helper to parse latitude
    stop_lon = gtfs.parse_longitude(columns[5])  # Use helper to parse longitude
    zone_id = columns[6]
    stop_url = gtfs.parse_url(columns[7])  # Use helper to parse URL
    location_type = gtfs.parse_location_type(columns[8])  # Use helper to parse location type
    parent_station = columns[9]  # Generating new UniqueID for parent station
    wheelchair_boarding = gtfs.parse_wheelchair_boarding(columns[10])  # Use helper to parse wheelchair boarding

    # Return a Stop instance
    return Stop(
        stop_id=stop_id,
        stop_code=stop_code,
        stop_name=stop_name,
        stop_desc=stop_desc,
        stop_lat=stop_lat,
        stop_lon=stop_lon,
        zone_id=zone_id,
        stop_url=stop_url,
        location_type=location_type,
        parent_station=parent_station,
        wheelchair_boarding=wheelchair_boarding
    )


if __name__ == "__main__":
    with open("stops.txt", 'r') as file:
        lines = file.readlines()
        stops = gtfs.parse(lines[1:], parse_row_to_stop)
        print(f"There were {len(stops)} stops.")

        def query(**kwargs):
            """
            Purpose: Convenience function for querying stops.
            Examples:
                query(stop_name="Westbound Davie St @ Bidwell St")
                query(stop_code="50011")
            """
            for s in gtfs.query(stops, **kwargs):
                print(s)
    
    


