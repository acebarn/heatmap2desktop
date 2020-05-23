# Strava Heatmap2Desktop

Python tool to generate customizable desktop background image to show a heatmap of your recent activities.
All you need to do is to get personal Strava API credentials and run the script with your desired configuration.

This Project is based on this repository: https://github.com/remisalmon/Strava-local-heatmap

### Command-line options

```
main.py [-h] 
        [--count COUNT] 
        [--gpx-dir DIR]
        [--bounds LAT_BOTTOM LAT_TOP LON_LEFT LON_RIGHT] 
        [--output OUTPUT]      
        [--zoom ZOOM]

optional arguments:
  -h, --help            show this help message and exit
  --count COUNT         Number of recent activities to include (default: 30) 
  --gpx-dir DIR         GPX files directory (default: gpx)
  --bounds LAT_BOTTOM LAT_TOP LON_LEFT LON_RIGHT
                        heatmap bounding box coordinates as lat_min, lat_max,
                        lon_min, lon_max (default: 48, 50, 7, 10 => Karlsruhe,
                        Germany)
  --output OUTPUT       heatmap name (default: heatmap.png)
  --zoom ZOOM           heatmap zoom level 0-19 as used on openstreetmap.org (default: 13)
```

Example:  
`python3 main.py --count 100 --output myheatmap.png --bounds 48.667 49.43 7.49 9.12 --zoom 12 --gpx-dir ~/gpx`

## Setup

Run `bash setup.sh && source virtualenv/bin/activate`

Create a strava App here: http://strava.com/settings/api
Once you got your `client-id` and `client-secret` paste them into the provided `config.yml` file.

### Python dependencies

```
matplotlib==3.1.1
numpy==1.17.3
certifi==2020.4.5.1
urllib3==1.25.9
oauth2==1.9.0.post1
pyyaml==5.3.1
```

### Troubleshooting

## Authorization Errors with the Strava API
Delete the `access.token` file