import io
import logging
from concurrent.futures import ThreadPoolExecutor

import geopandas as gpd
import matplotlib.pyplot as plt
import odc
import odc.stac
import pandas as pd
import planetary_computer
import pystac
import pystac_client
import rioxarray  # noqa: F401
import xarray as xr
from shapely.geometry import Polygon
from tqdm.auto import tqdm

logger = logging.getLogger(__name__)


class Sentinel2:
    def __init__(self):
        logger.debug("Initializing Sentinel2 client")
        self.catalog = pystac_client.Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace,
        )

    def get_items(
        self,
        start_date: str,
        end_date: str,
        polygon: dict,
        entire_image_cloud_cover_threshold: int = 20,
    ) -> list[pystac.Item]:
        """
        Search for Sentinel-2 items within a given date range and polygon.

        Args:
            start_date: Start date for the search (YYYY-MM-DD)
            end_date: End date for the search (YYYY-MM-DD)
            polygon: GeoJSON polygon to intersect with the search
            entire_image_cloud_cover_threshold: Maximum cloud cover percentage to include in the search
            cropped_image_cloud_cover_threshold: Maximum cloud cover within a cropped image to include in the search

        Returns:
            List of STAC items matching the search criteria
        """
        logger.info(
            f"Searching for Sentinel-2 items between {start_date} and {end_date}"
        )
        search = self.catalog.search(
            collections=["sentinel-2-l2a"],
            datetime=f"{start_date}/{end_date}",
            intersects=polygon,
            query={"eo:cloud_cover": {"lt": entire_image_cloud_cover_threshold}} if entire_image_cloud_cover_threshold else None,
        )
        items = search.item_collection()
        logger.info(f"Found {len(items)} items")
        return items

    def load_xarray(
        self,
        start_date: str,
        end_date: str,
        polygon: dict,
        entire_image_cloud_cover_threshold: int = 20,
        cropped_image_cloud_cover_threshold: int = 80,
        bands: list[str] = ["B02", "B03", "B04", "B08"],
        resolution: int = 10,
        max_workers: int = 10,
        show_progress: bool = True,
        filter_cloud_cover: bool = True,
    ) -> xr.Dataset:
        """Load Sentinel-2 data for a given date range and polygon into an xarray Dataset.

        Args:
            start_date: Start date for the search (YYYY-MM-DD)
            end_date: End date for the search (YYYY-MM-DD)
            polygon: GeoJSON polygon to intersect with the search
            bands: List of band names to load. Defaults to ["B02", "B03", "B04", "B08"]
            resolution: Resolution in meters. Defaults to 10
            max_workers: Maximum number of workers to use for loading the data
            show_progress: Whether to show a progress bar
            filter_cloud_cover: Whether to filter the data based on cloud cover
            entire_image_cloud_cover_threshold: Maximum cloud cover percentage to include in the search
            cropped_image_cloud_cover_threshold: Maximum cloud cover within a cropped image to include in the search

        Returns:
            xarray Dataset containing the Sentinel-2 data
        """
        logger.info(
            f"Loading Sentinel-2 data for bands {bands} at {resolution}m resolution"
        )
        items = self.get_items(
            start_date=start_date,
            end_date=end_date,
            polygon=polygon,
            entire_image_cloud_cover_threshold=entire_image_cloud_cover_threshold,
        )

        if not items:
            logger.error(
                "No Sentinel-2 items found for the given date range and polygon"
            )
            raise ValueError(
                "No Sentinel-2 items found for the given date range and polygon"
            )

        # Sign the items to get access
        logger.info("Signing items for access")
        signed_items = [planetary_computer.sign(item) for item in items]
        thread_pool = ThreadPoolExecutor(max_workers=max_workers)

        # Load the data into an xarray Dataset
        logger.info("Loading data into xarray Dataset")
        progress = tqdm
        ds = odc.stac.load(
            signed_items,
            bands=bands + ["SCL"],
            resolution=resolution,
            pool=thread_pool,
            geopolygon=polygon,
            progress=progress if show_progress else None,
        )
        
        if cropped_image_cloud_cover_threshold:
            logger.debug("Filtering data based on cloud cover using SCL band")
            cloud_clear_mask = (ds.SCL == 4) | (ds.SCL == 5)
            cloud_cover_pct = (1 - cloud_clear_mask.mean(dim=['x', 'y'])) * 100
            logger.debug(f"Cloud cover percentage: {cloud_cover_pct}. Filtering data based on {cropped_image_cloud_cover_threshold}% cloud cover threshold")
            logger.info(f"Dataset time steps before filtering: {len(ds.time)}")
            ds = ds.sel(time=cloud_cover_pct <= cropped_image_cloud_cover_threshold)
            logger.info(f"Filtered dataset to {len(ds.time)} time steps based on {cropped_image_cloud_cover_threshold}% cloud cover threshold")
        
        if filter_cloud_cover:
            cloud_clear_mask = (ds.SCL == 4) | (ds.SCL == 5)
            ds = ds.where(cloud_clear_mask, drop=True) 

        logger.info("Successfully loaded Sentinel-2 data")
        return ds

    def load_ndvi_images(
        self,
        start_date: str,
        end_date: str,
        polygon: dict,
        entire_image_cloud_cover_threshold: int = 20,
        cropped_image_cloud_cover_threshold: int = 80,
        max_workers: int = 10,
        filter_cloud_cover: bool = True,
    ) -> xr.Dataset:
        """Load NDVI data for a given date range and polygon.

        Args:
            start_date: Start date for the search (YYYY-MM-DD)
            end_date: End date for the search (YYYY-MM-DD)
            polygon: GeoJSON polygon to intersect with the search
            max_workers: Maximum number of workers to use for loading the data
            entire_image_cloud_cover_threshold: Maximum cloud cover percentage to include in the search
            cropped_image_cloud_cover_threshold: Maximum cloud cover within a cropped image to include in the search

        Returns:
            xarray Dataset containing the NDVI data
        """
        logger.info("Loading NDVI data")
        ds = self.load_xarray(
            start_date=start_date,
            end_date=end_date,
            polygon=polygon,
            entire_image_cloud_cover_threshold=entire_image_cloud_cover_threshold,
            cropped_image_cloud_cover_threshold=cropped_image_cloud_cover_threshold,
            max_workers=max_workers,
            bands=["B08", "B04"],
            filter_cloud_cover=filter_cloud_cover,
        )
        logger.debug("Calculating NDVI from bands B08 and B04")
        ndvi = (ds.B08 - ds.B04) / (ds.B08 + ds.B04)
        logger.info("Successfully calculated NDVI")
        return ndvi
    
    @staticmethod
    def ndvi_thumbnails(
        ndvi: xr.DataArray,
        polygon: dict,
        polygon_crs: str,
        vmin: float = -0.2,
        vmax: float = 0.8,
        boundary_color: str = 'red',
        boundary_linewidth: float = 2,
        add_colorbar: bool = False,
        add_labels: bool = False,
        bbox_inches: str = 'tight',
        pad_inches: float = 0,
        image_format: str = 'jpg',
        timestamp_format: str = '%Y-%m-%d'
    ) -> dict:
        """
        Plot NDVI images and return them as jpgs in a dictionary
        
        Args:
            ndvi: xarray DataArray containing NDVI data
            polygon: GeoJSON polygon used for the data fetch
            crs: Coordinate reference system of the NDVI data
            figsize: Figure size as (width, height) tuple
            vmin: Minimum value for NDVI color scale
            vmax: Maximum value for NDVI color scale
            boundary_color: Color of the polygon boundary
            boundary_linewidth: Line width of the polygon boundary
            add_colorbar: Whether to add a colorbar to the plot
            add_labels: Whether to add labels to the plot
            bbox_inches: Bounding box setting for saving figure
            pad_inches: Padding when saving figure
            image_format: Format to save images in
            timestamp_format: Format string for timestamp keys
            
        Returns:
            dict: Dictionary with timestamps as keys and image bytes as values
        """
        images = {}
        
        # Convert polygon coordinates to shapely Polygon
        coords = polygon['geometry']['coordinates'][0]
        poly = Polygon(coords)
        gdf = gpd.GeoDataFrame(geometry=[poly], crs=polygon_crs)
        crs = ndvi.coords["spatial_ref"].values.item()
        gdf = gdf.to_crs(crs)  # Convert to UTM zone 32N to match the NDVI data

        for time in ndvi.time:
            # Create new figure for each timestamp
            fig, ax = plt.subplots()
            
            # Plot NDVI data and polygon boundary
            ndvi.sel(time=time).plot(ax=ax, vmin=vmin, vmax=vmax, 
                                   add_colorbar=add_colorbar, add_labels=add_labels)
            gdf.boundary.plot(ax=ax, color=boundary_color, linewidth=boundary_linewidth)
            ax.set_axis_off()
            
            # Save plot to bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format=image_format, bbox_inches=bbox_inches, pad_inches=pad_inches)
            buf.seek(0)
            
            # Add to dictionary with timestamp as key
            timestamp = pd.Timestamp(time.values).strftime(timestamp_format)
            images[timestamp] = buf.getvalue()
            
            # Close figure to free memory
            plt.close(fig)
            
        return images
    
    @staticmethod
    def calculate_mean_ndvi(
        ndvi_images: xr.Dataset,
        polygon: dict,
        polygon_crs: str,
        interpolate: bool = False,
        start_date: str = None,
        end_date: str = None,
    ) -> pd.DataFrame:
        """
        Calculate mean NDVI value for the given polygon at each timestamp
        
        Args:
            ndvi_images (xarray.Dataset): NDVI data
            polygon (dict): GeoJSON polygon
            
        Returns:
            dict: Mapping of timestamps to mean NDVI values
        """
        logger.info("Calculating mean NDVI values for polygon")
        
        # Convert to rioxarray and clip once for all timestamps
        crs = ndvi_images.coords["spatial_ref"].values.item()
    
        
        ndvi_images = ndvi_images.rio.write_crs(crs)
        clipped_data = ndvi_images.rio.clip([polygon["geometry"]], polygon_crs)
        
        # Calculate means for all timestamps at once
        mean_values = clipped_data.mean(dim=['x', 'y']).values
        
        # Create dictionary mapping timestamps to means
        mean_ndvi = pd.DataFrame(mean_values,  columns=['mean_ndvi'], index=clipped_data.time.values)
        mean_ndvi.index = pd.to_datetime(mean_ndvi.index).date
        if interpolate:
            if not (start_date or end_date):
                raise ValueError("Interpolation requires start_date and end_date")
            else:
                mean_ndvi = interpolate_ndvi(mean_ndvi, start_date, end_date)
        
        logger.info(f"Calculated mean NDVI for {len(mean_ndvi)} timestamps")
        return mean_ndvi
    

def interpolate_ndvi(df: pd.DataFrame, start_date: str, end_date: str):
    """
    Create a DataFrame from NDVI values, interpolate missing dates, and plot the results.
    
    Args:
        mean_ndvi_values (dict): Dictionary of dates and NDVI values
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        
    Returns:
        pd.DataFrame: DataFrame with interpolated daily NDVI values
    """
    date_range = pd.date_range(start=pd.to_datetime(start_date), end=pd.to_datetime(end_date), freq='D')
    df = df.reindex(date_range).interpolate(method='linear', limit_direction='both')
    return df