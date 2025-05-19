from typing import List, Dict, Optional
from pydantic import Field
# from . import Stop, Route, Trip, StopTime
from .. import SumGtfsBaseModel
from shapely.geometry import Point, LineString, mapping
import geopandas as gpd
from . import Stop, Route, Trip, StopTime
from collections import defaultdict
import json

class GTFSNetwork(SumGtfsBaseModel):
    """
    Represents the full public transport network described by GTFS files.

    Attributes:
        stops: All GTFS stops (stations or platforms).
        routes: All GTFS routes (lines).
        trips: All trips (vehicle runs) along routes.
        stop_times: Stop-by-stop itineraries for each trip.
    """
    stops: List[Stop] = Field(default_factory=list)
    routes: List[Route] = Field(default_factory=list)
    trips: List[Trip] = Field(default_factory=list)
    stop_times: List[StopTime] = Field(default_factory=list)

    def stops_to_geojson(self, filepath: str):
        """
        Export stops as a GeoJSON file, with stop information as properties.
        """
        if not self.stops:
            return
        gdf = gpd.GeoDataFrame(
            [s.model_dump() for s in self.stops],
            geometry=[Point(s.stop_lon, s.stop_lat) for s in self.stops if s.stop_lon is not None and s.stop_lat is not None],
            crs="EPSG:4326"
        )
        gdf.to_file(filepath, driver="GeoJSON")
        
    def OLD_itineraries_to_geojson(self, filepath: str):
        """
        Export each route's itinerary as a GeoJSON LineString, using stop sequences for each trip.
        Each feature represents a trip (vehicle run) along a route, with properties for route_id, trip_id, and stop sequence.
        """
        if not self.trips or not self.stop_times or not self.stops:
            return

        # Build a lookup for stop_id -> (lon, lat)
        stop_lookup = {stop.stop_id: (stop.stop_lon, stop.stop_lat) for stop in self.stops if stop.stop_lon is not None and stop.stop_lat is not None}

        features = []
        for trip in self.trips:
            # Get all stop_times for this trip, ordered by stop_sequence
            trip_stop_times = [st for st in self.stop_times if st.trip_id == trip.trip_id]
            trip_stop_times.sort(key=lambda st: st.stop_sequence)
            coords = []
            for st in trip_stop_times:
                coord = stop_lookup.get(st.stop_id)
                if coord:
                    coords.append(coord)
            if len(coords) >= 2:
                features.append({
                    "route_id": getattr(trip, "route_id", None),
                    "trip_id": trip.trip_id,
                    "geometry": LineString(coords),
                    "stop_sequence": [st.stop_id for st in trip_stop_times]
                })

        if not features:
            return

        gdf = gpd.GeoDataFrame(
            features,
            geometry="geometry",
            crs="EPSG:4326"
        )
        gdf.to_file(filepath, driver="GeoJSON")
        
    def itineraries_to_geojson(self, filepath) -> Dict:
        """
        Generates a GeoJSON FeatureCollection of route itineraries using stop sequences
        from GTFS trips and stop_times. One feature per route_id + direction_id.

        Returns:
            A GeoJSON FeatureCollection dictionary.
        """
        print("Exporting itineraries to GeoJSON...")
        # Map stop_id to coordinates
        stop_coords = {stop.stop_id: [stop.stop_lon, stop.stop_lat] for stop in self.stops}

        # Group stop_times by trip_id
        trip_stop_times: Dict[str, List[StopTime]] = defaultdict(list)
        for st in self.stop_times:
            trip_stop_times[st.trip_id].append(st)

        # Group trips by (route_id, direction_id) and pick first trip as representative
        trip_by_route_dir: Dict[tuple, Trip] = {}
        for trip in self.trips:
            key = (trip.route_id, trip.direction_id or 0)
            if key not in trip_by_route_dir:
                trip_by_route_dir[key] = trip

        # Map route_id to route for metadata
        route_lookup = {route.route_id: route for route in self.routes}

        features = []

        for (route_id, direction_id), trip in trip_by_route_dir.items():
            stop_times = sorted(trip_stop_times.get(trip.trip_id, []), key=lambda st: st.stop_sequence)
            coords = [stop_coords[st.stop_id] for st in stop_times if st.stop_id in stop_coords]

            if len(coords) < 2:
                continue  # Skip invalid or empty lines

            route = route_lookup.get(route_id)

            properties = {
                "route_id": route.route_id if route else route_id,
                "route_short_name": route.route_short_name if route else None,
                "route_long_name": route.route_long_name if route else None,
                "route_type": route.route_type if route else None,
                "direction_id": direction_id,
                "trip_id": trip.trip_id,
                "headsign": trip.trip_headsign,
                "color": route.route_color if route else None,
                "text_color": route.route_text_color if route else None,
            }

            feature = {
                "type": "Feature",
                "geometry": mapping(LineString(coords)),
                "properties": properties
            }

            features.append(feature)

        #save to file filepath
        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }
        with open(filepath, 'w') as f:
            json.dump(feature_collection, f, indent=4)
        print(f"Exported {len(features)} itineraries to {filepath}")
        # gdf = gpd.GeoDataFrame(
        #     features,
        #     geometry="geometry",
        #     crs="EPSG:4326"
        # )
        # gdf.to_file(filepath, driver="GeoJSON")