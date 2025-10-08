# Google Earth Engine Setup Guide

## Why Use Google Earth Engine for MODIS Data?

Google Earth Engine (GEE) is much better than NASA LAADS DAAC for MODIS data because:

- ✅ **Pre-processed data** - No raw HDF files to download and process
- ✅ **Cloud-based processing** - No local storage requirements  
- ✅ **Built-in filtering** - Date, cloud cover, and quality filters
- ✅ **Direct analysis** - Process data directly in the cloud
- ✅ **Free for research** - No API limits
- ✅ **Better documentation** - More examples and tutorials

## Setup Instructions

### 1. Create Google Earth Engine Account

1. Go to [https://earthengine.google.com/](https://earthengine.google.com/)
2. Sign up with your Google account
3. Request access (usually approved within 24-48 hours for academic use)

### 2. Install Google Earth Engine Python API

```bash
pip install earthengine-api
```

### 3. Authenticate

Run this command in your terminal:

```bash
earthengine authenticate
```

This will:
- Open your browser
- Ask you to sign in to your Google account
- Generate authentication credentials
- Save them locally

### 4. Test Connection

Run the test script:

```bash
python src/gee_data_acquisition.py
```

## Available MODIS Products in GEE

| Product | Description | Resolution |
|---------|-------------|------------|
| `MODIS/006/MOD04_3K` | Terra AOD 3km | 3km |
| `MODIS/006/MYD04_3K` | Aqua AOD 3km | 3km |
| `MODIS/006/MOD06_L2` | Terra Cloud Properties | 1km |
| `MODIS/006/MYD06_L2` | Aqua Cloud Properties | 1km |
| `MODIS/006/MOD08_D3` | Terra Daily Atmosphere | 1° |
| `MODIS/006/MYD08_D3` | Aqua Daily Atmosphere | 1° |

## Usage Example

```python
from src.gee_data_acquisition import GEEDataAcquisition

# Initialize GEE
gee = GEEDataAcquisition()

# Get AOD data for Mediterranean region
mediterranean_bbox = [5, 30, 40, 50]  # [min_lon, min_lat, max_lon, max_lat]

# Get AOD collection
aod_collection = gee.get_modis_aod_collection(
    start_date='2020-06-01',
    end_date='2020-06-30',
    bbox=mediterranean_bbox
)

# Extract statistics
aod_stats = gee.extract_aod_statistics(aod_collection, mediterranean_bbox)

# Detect dust events
dust_events = gee.detect_dust_events(aod_stats)

print(f"Found {len(dust_events)} dust events")
```

## Advantages for Your Study

1. **No data download** - Process directly in the cloud
2. **Automatic quality filtering** - Built-in cloud cover and quality filters
3. **Easy temporal analysis** - Built-in date filtering and aggregation
4. **Scalable processing** - Handle large datasets without memory issues
5. **Integrated analysis** - Combine with other datasets (ERA5, etc.)

## Next Steps

1. Set up GEE account and authentication
2. Test the connection
3. Use GEE for MODIS data instead of NASA LAADS DAAC
4. Focus on dust event detection and temporal analysis
