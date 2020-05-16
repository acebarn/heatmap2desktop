import argparse
import heatmap_generator as hmg


def main():
    print("Starting heatmap generation")

    #Download activities from strava

    #store activities in gpx folder

    #call heatmap generator to produce png
    hmg.generate_heatmap("gpx", "all", [48.667,49.43,7.49,9.12],"output",13)
    

    print("finished!")

if __name__ == '__main__':
    # command line parameters
    # parser = argparse.ArgumentParser(description = 'Generate a local heatmap from Strava GPX files', epilog = 'Report issues to https://github.com/remisalmon/strava-local-heatmap')

    # parser.add_argument('--gpx-dir', dest = 'dir', default = 'gpx', help = 'GPX files directory  (default: gpx)')
    # parser.add_argument('--gpx-year', dest = 'year', default = 'all', help = 'GPX files year filter (default: all)')
    # parser.add_argument('--gpx-filter', dest = 'glob', default = '*.gpx', help = 'GPX files glob filter (default: *.gpx)')
    # parser.add_argument('--gpx-bound', dest = 'bound', type = float, nargs = 4, default = [-90, +90, -180, +180], help = 'heatmap bounding box coordinates as lat_min, lat_max, lon_min, lon_max (default: -90 +90 -180 +180)')
    # parser.add_argument('--output', dest = 'file', default = 'heatmap.png', help = 'heatmap name (default: heatmap.png)')
    # parser.add_argument('--zoom', dest = 'zoom', type = int, default = 10, help = 'heatmap zoom level 0-19 (default: 10)')

    # args = parser.parse_args()

    # run main
    main()