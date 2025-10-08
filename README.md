# Dust Persistence Study

**Temporal Persistence of Dust-Induced Cloud Microphysical Anomalies over the Mediterranean Basin (2002-2022)**

## Project Overview

This study investigates the temporal persistence of cloud microphysical changes following Saharan dust intrusion events over the Mediterranean Basin. The research aims to quantify how long dust-induced cloud anomalies persist and identify the factors controlling this persistence.

## Research Questions

1. How long do dust-induced cloud microphysical anomalies persist after dust arrival?
2. What factors control the persistence duration and decay rate?
3. When are the effects most detectable and statistically significant?

## Project Structure

```
dust_persistence_study/
├── data/                          # Data storage
│   ├── raw/                       # Raw satellite and reanalysis data
│   └── processed/                 # Processed datasets
│       ├── dust_events/           # Dust event catalog
│       ├── cloud_anomalies/       # Cloud property anomalies
│       └── persistence_metrics/   # Persistence statistics
├── src/                           # Source code
│   ├── data_acquisition.py        # Data download and preprocessing
│   ├── event_detection.py         # Dust event detection algorithm
│   ├── temporal_analysis.py       # Temporal tracking and analysis
│   ├── statistical_analysis.py    # Statistical modeling
│   └── visualization.py           # Plotting and visualization
├── notebooks/                     # Jupyter notebooks for analysis
├── config/                        # Configuration files
│   └── study_config.yaml          # Main study configuration
├── results/                       # Results and outputs
│   ├── figures/                   # Plots and visualizations
│   └── tables/                    # Statistical tables
└── docs/                          # Documentation
```

## Data Sources

- **MODIS**: Aerosol Optical Depth (AOD) and cloud properties
- **CALIOP**: Aerosol type classification and vertical profiling
- **ERA5**: Meteorological reanalysis data
- **HYSPLIT**: Back-trajectory analysis

## Methodology

1. **Event Detection**: Identify dust intrusion events using AOD thresholds and CALIOP validation
2. **Temporal Tracking**: Monitor cloud properties for 7 days following dust arrival
3. **Anomaly Calculation**: Compute cloud property anomalies relative to climatology
4. **Persistence Analysis**: Quantify duration and decay rates of anomalies
5. **Statistical Modeling**: Identify controlling factors using regression analysis

## Installation

```bash
# Clone the repository
git clone https://github.com/HoriaCama99/Paper2025.git
cd Paper2025

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config/study_config.yaml.example config/study_config.yaml
```

## Usage

```python
from src import DataAcquisition, DustEventDetector, TemporalAnalyzer

# Initialize components
da = DataAcquisition()
detector = DustEventDetector()
analyzer = TemporalAnalyzer()

# Run analysis pipeline
events = detector.detect_events()
persistence = analyzer.analyze_persistence(events)
```

## Expected Outcomes

- Comprehensive dust event catalog (2002-2022)
- Quantified persistence statistics and decay rates
- Identification of controlling meteorological factors
- Manuscript for peer-reviewed publication

## Author

**Horia Camarasan**  
PhD Candidate, UBB  
Email: horia.camarasan@ubbcluj.ro

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NASA for MODIS and CALIOP data
- ECMWF for ERA5 reanalysis
- NOAA for HYSPLIT trajectory model
