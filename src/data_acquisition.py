"""
Data Acquisition Module

Handles downloading and preprocessing of satellite and reanalysis data
for the dust persistence study.

Author: Horia Camarasan
"""

import os
import requests
import yaml
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import cdsapi
import h5py
from tqdm import tqdm
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataAcquisition:
    """
    Handles data acquisition from various sources including MODIS, CALIOP, and ERA5.
    """
    
    def __init__(self, config_path="config/study_config.yaml"):
        """
        Initialize data acquisition with configuration.
        
        Parameters:
        -----------
        config_path : str
            Path to configuration file
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.data_dir = Path(self.config['paths']['data_dir'])
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize CDS API client for ERA5
        self.cds_client = cdsapi.Client()
        
    def get_modis_aod(self, date, bbox=None):
        """
        Download MODIS AOD data for a specific date.
        
        Parameters:
        -----------
        date : datetime
            Date for data download
        bbox : list, optional
            Bounding box [min_lon, min_lat, max_lon, max_lat]
            
        Returns:
        --------
        str : Path to downloaded file
        """
        if bbox is None:
            bbox = self.config['study_domain']['bbox']
            
        url = "https://ladsweb.modaps.eosdis.nasa.gov/api/v2/content/details"
        params = {
            'products': 'MCD19A2',
            'collection': self.config['data_sources']['modis']['collection'],
            'date': date.strftime('%Y-%m-%d'),
            'bbox': ','.join(map(str, bbox))
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # Save response to file
            filename = f"modis_aod_{date.strftime('%Y%m%d')}.hdf"
            filepath = self.raw_dir / "modis_aod" / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            logger.info(f"Downloaded MODIS AOD data for {date.strftime('%Y-%m-%d')}")
            return str(filepath)
            
        except requests.RequestException as e:
            logger.error(f"Failed to download MODIS AOD data: {e}")
            return None
    
    def get_modis_cloud(self, date, satellite='Terra'):
        """
        Download MODIS cloud properties data.
        
        Parameters:
        -----------
        date : datetime
            Date for data download
        satellite : str
            'Terra' or 'Aqua'
            
        Returns:
        --------
        str : Path to downloaded file
        """
        product = 'MOD06_L2' if satellite == 'Terra' else 'MYD06_L2'
        
        url = "https://ladsweb.modaps.eosdis.nasa.gov/api/v2/content/details"
        params = {
            'products': product,
            'collection': self.config['data_sources']['modis']['collection'],
            'date': date.strftime('%Y-%m-%d')
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            filename = f"modis_cloud_{satellite.lower()}_{date.strftime('%Y%m%d')}.hdf"
            filepath = self.raw_dir / "modis_cloud" / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            logger.info(f"Downloaded MODIS cloud data for {satellite} on {date.strftime('%Y-%m-%d')}")
            return str(filepath)
            
        except requests.RequestException as e:
            logger.error(f"Failed to download MODIS cloud data: {e}")
            return None
    
    def get_era5_data(self, date, variables=None, pressure_levels=None):
        """
        Download ERA5 reanalysis data.
        
        Parameters:
        -----------
        date : datetime
            Date for data download
        variables : list, optional
            List of variables to download
        pressure_levels : list, optional
            List of pressure levels for pressure-level data
            
        Returns:
        --------
        str : Path to downloaded file
        """
        if variables is None:
            variables = self.config['data_sources']['era5']['variables']
            
        area = self.config['study_domain']['bbox']  # [N, W, S, E]
        
        try:
            # Determine if we need single-level or pressure-level data
            if pressure_levels is not None:
                dataset_name = 'reanalysis-era5-pressure-levels'
                request_params = {
                    'product_type': 'reanalysis',
                    'variable': variables,
                    'pressure_level': pressure_levels,
                    'year': date.year,
                    'month': f"{date.month:02d}",
                    'day': f"{date.day:02d}",
                    'time': ['00:00', '06:00', '12:00', '18:00'],
                    'area': area,
                    'format': 'netcdf'
                }
                filename = f"era5_pressure_{date.strftime('%Y%m%d')}.nc"
            else:
                dataset_name = 'reanalysis-era5-single-levels'
                request_params = {
                    'product_type': 'reanalysis',
                    'variable': variables,
                    'year': date.year,
                    'month': f"{date.month:02d}",
                    'day': f"{date.day:02d}",
                    'time': ['00:00', '06:00', '12:00', '18:00'],
                    'area': area,
                    'format': 'netcdf'
                }
                filename = f"era5_single_{date.strftime('%Y%m%d')}.nc"
            
            result = self.cds_client.retrieve(dataset_name, request_params)
            
            filepath = self.raw_dir / "era5" / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            result.download(str(filepath))
            logger.info(f"Downloaded ERA5 data for {date.strftime('%Y-%m-%d')}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Failed to download ERA5 data: {e}")
            return None
    
    def extract_caliop_dust(self, caliop_file):
        """
        Extract dust information from CALIOP data.
        
        Parameters:
        -----------
        caliop_file : str
            Path to CALIOP HDF file
            
        Returns:
        --------
        dict : Extracted dust information
        """
        try:
            with h5py.File(caliop_file, 'r') as f:
                # Extract aerosol type (1=dust, 2=smoke, 3=polluted dust, etc.)
                aerosol_type = f['/Aerosol_Type_532'][:]
                # Extract AOD
                aod = f['/Extinction_Coefficient_532'][:]
                # Extract latitude and longitude
                lat = f['/Latitude'][:]
                lon = f['/Longitude'][:]
                
                return {
                    'aerosol_type': aerosol_type,
                    'aod': aod,
                    'latitude': lat,
                    'longitude': lon
                }
                
        except Exception as e:
            logger.error(f"Failed to extract CALIOP data: {e}")
            return None
    
    def download_time_series(self, start_date, end_date, data_types=['modis_aod', 'era5']):
        """
        Download data for a time series.
        
        Parameters:
        -----------
        start_date : datetime
            Start date for download
        end_date : datetime
            End date for download
        data_types : list
            Types of data to download
            
        Returns:
        --------
        list : List of downloaded file paths
        """
        downloaded_files = []
        current_date = start_date
        
        # Create progress bar
        total_days = (end_date - start_date).days + 1
        pbar = tqdm(total=total_days, desc="Downloading data")
        
        while current_date <= end_date:
            # Skip if not in focus months
            if current_date.month not in self.config['time_period']['focus_months']:
                current_date += timedelta(days=1)
                pbar.update(1)
                continue
                
            for data_type in data_types:
                if data_type == 'modis_aod':
                    filepath = self.get_modis_aod(current_date)
                elif data_type == 'modis_cloud':
                    filepath = self.get_modis_cloud(current_date)
                elif data_type == 'era5':
                    filepath = self.get_era5_data(current_date)
                
                if filepath:
                    downloaded_files.append(filepath)
            
            current_date += timedelta(days=1)
            pbar.update(1)
        
        pbar.close()
        logger.info(f"Downloaded {len(downloaded_files)} files")
        return downloaded_files
    
    def preprocess_modis_data(self, filepath):
        """
        Preprocess MODIS data to extract relevant variables.
        
        Parameters:
        -----------
        filepath : str
            Path to MODIS file
            
        Returns:
        --------
        xarray.Dataset : Preprocessed data
        """
        try:
            # Read MODIS data (this is a simplified example)
            # In practice, you'd use specific MODIS readers like pyhdf or similar
            ds = xr.open_dataset(filepath)
            
            # Extract and rename variables
            processed_ds = xr.Dataset({
                'aod': ds['AOD_550_Dark_Target_Deep_Blue_Combined'],
                'latitude': ds['lat'],
                'longitude': ds['lon']
            })
            
            # Apply quality flags and filters
            # This would depend on the specific MODIS product
            
            return processed_ds
            
        except Exception as e:
            logger.error(f"Failed to preprocess MODIS data: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    da = DataAcquisition()
    
    # Download data for a single day
    test_date = datetime(2020, 6, 15)
    aod_file = da.get_modis_aod(test_date)
    era5_file = da.get_era5_data(test_date)
    
    print(f"Downloaded files: {aod_file}, {era5_file}")
