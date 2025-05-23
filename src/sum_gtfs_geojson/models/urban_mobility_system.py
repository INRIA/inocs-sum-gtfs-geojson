from typing import List, Optional
from .sum_gtfs_base_model import SumGtfsBaseModel
from .gtfs import Stop, Route, GTFSNetwork
from .gbfs import StationInfoStatus
from .mobility import BikeTrip, Ridership
from .grid import HexGrid
from pydantic import Field
import os
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point, LineString


class UrbanMobilitySystem(SumGtfsBaseModel):
    """
    Represents an integrated urban mobility system, combining public transport,
    bike sharing infrastructure, and observed user demand.

    Attributes:
        public_transport: GTFS-defined public transport network.
        bike_stations: Metadata for bike sharing stations, including status and inventory.
        ridership: Observed passenger activity at public transport stops, inflow and outflow.
        bike_trips: Individual shared-bike trips with spatial and temporal metadata.
    """
    public_transport: GTFSNetwork = Field(
        ..., description="GTFS-defined public transport network.")
    bike_stations: List[StationInfoStatus] = Field(
        ..., description="Custom GBFS Bike sharing station infrastructure metadata, with status (inventory...) over time periods.")
    ridership: List[Ridership] = Field(
        ..., description="Passenger activity at transit stops (e.g., boardings).")
    bike_trips: List[BikeTrip] = Field(
        ..., description="Trip-level data from bike sharing systems.")

    hex_grid: Optional[HexGrid] = Field(
        None, description="Hexagonal grid for spatial analysis.")

    def save_to_geojson(self, output_path: str = "data/sum_gtfs_geojson/geojson"):
        """
        Save the Urban Mobility System data to GeoJSON files. One file per data type.
        The files will be saved in the specified output path.
        :param output_path: The path where the GeoJSON files will be saved. Default is "data/sum_gtfs_geojson/geojson".
        """
        Path(output_path).mkdir(parents=True, exist_ok=True)

        # Save each layer as a separate GeoJSON file
        self.stops_to_geojson(os.path.join(output_path, "stops.geojson"))
        self.itineraries_to_geojson(os.path.join(output_path, "itineraries.geojson"))
        self.bike_stations_to_geojson(os.path.join(
            output_path, "bike_stations.geojson"))
        self.ridership_to_geojson(os.path.join(
            output_path, "ridership.geojson"))
        self.bike_trips_to_geojson(os.path.join(
            output_path, "bike_trips.geojson"))
        self.hex_grid_to_geojson(os.path.join(
            output_path, "hex_grid.geojson"))
        print(f"GeoJSON files saved to {output_path}")

    def stops_to_geojson(self, filepath):
        """
        Export stops as a GeoJSON file, with stop information as properties.
        Args:
            filepath (str): The path to the output GeoJSON file.
        """
        print("Exporting stops to GeoJSON...")
        self.public_transport.stops_to_geojson(filepath)

    def itineraries_to_geojson(self, filepath):
        """
        Export each route's itinerary as a GeoJSON LineString, using stop sequences for each trip.

        Args:
            filepath (str): The path to the output GeoJSON file.
        """
        print("Exporting routes to GeoJSON...")
        self.public_transport.itineraries_to_geojson(filepath)

    def bike_stations_to_geojson(self, filepath):
        """
        Export bike stations as a GeoJSON file, with station information as properties.
        Args:
            filepath (str): The path to the output GeoJSON file.
        """
        print("Exporting bike stations to GeoJSON...")
        if not self.bike_stations:
            return
        gdf = gpd.GeoDataFrame(
            [s.model_dump() for s in self.bike_stations],
            geometry=[Point(s.lon, s.lat)
                      for s in self.bike_stations if s.lon is not None and s.lat is not None],
            crs="EPSG:4326"
        )
        gdf.to_file(filepath, driver="GeoJSON")

        return gdf

    def ridership_to_geojson(self, filepath):
        """
        Export ridership data as a GeoJSON file, with stop information as properties.
        Args:
            filepath (str): The path to the output GeoJSON file.
        """
        print("Exporting ridership to GeoJSON...")
        if not self.ridership:
            return
        gdf = gpd.GeoDataFrame(
            [r.model_dump() for r in self.ridership],
            geometry=[Point(r.stop_lon, r.stop_lat)
                      for r in self.ridership if r.stop_lon is not None and r.stop_lat is not None],
            crs="EPSG:4326"
        )
        gdf.to_file(filepath, driver="GeoJSON")

    def bike_trips_to_geojson(self, filepath):
        """
        Export bike trips as a GeoJSON file, with trip information as properties.
        Args:
            filepath (str): The path to the output GeoJSON file.
        """
        print("Exporting bike trips to GeoJSON...")

        if not self.bike_trips:
            return
        # This assumes BikeTrip has latitude_start, longitude_start, latitude_end, longitude_end
        features = []
        for t in self.bike_trips:
            d = t.model_dump()
            if all([
                getattr(t, "longitude_start", None) is not None,
                getattr(t, "latitude_start", None) is not None,
                getattr(t, "longitude_end", None) is not None,
                getattr(t, "latitude_end", None) is not None,
            ]):
                d["geometry"] = LineString([
                    (t.longitude_start, t.latitude_start),
                    (t.longitude_end, t.latitude_end)
                ])
            else:
                d["geometry"] = None
            features.append(d)
        gdf = gpd.GeoDataFrame(
            features,
            geometry="geometry",
            crs="EPSG:4326"
        )
        gdf = gdf[gdf.geometry.notnull()]
        gdf.to_file(filepath, driver="GeoJSON")

    def hex_grid_to_geojson(self, filepath):
        """
        Export the hex grid to a GeoJSON file.
        Args:
            filepath (str): The path to the output GeoJSON file.
        """
        if not self.hex_grid:
            return
        self.hex_grid.to_geojson(filepath)
