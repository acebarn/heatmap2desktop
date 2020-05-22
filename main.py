import argparse
import heatmap_generator as hmg
import strava_export as strex


def main(args):
    print("Starting heatmap generation")

    _count = args.count
    _dir = args.dir
    _bounds = args.bounds
    _output = args.output
    _zoom = args.zoom

    #Download n activities from strava to specified location
    strex.export(int(_count), _dir)

    #call heatmap generator to produce png
    # hmg.generate_heatmap("gpx",[48.667,49.43,7.49,9.12],"output",13)
    hmg.generate_heatmap(_dir, _bounds, _output, _zoom)

    print("finished!")


if __name__ == '__main__':
    # command line parameters
    parser = argparse.ArgumentParser(
        description='Generate customizable desktop background image to show heatmap of recent strava activities',
        )

    parser.add_argument(
        '--count',
        dest='count',
        default='30',
        help='Number of recent activities to include (default: 30)')
    parser.add_argument('--gpx-dir',
                        dest='dir',
                        default='gpx',
                        help='GPX files directory  (default: gpx)')
    parser.add_argument(
        '--bounds',
        dest='bounds',
        type=float,
        nargs=4,
        default=[48, 50, 7, 10], #Karlsruhe
        help=
        'heatmap bounding box coordinates as LAT_BOTTOM, LAT_TOP, LON_LEFT, LON_RIGHT, (default: 48, 50, 7, 10 => Karlsruhe, Germany)'
    )
    parser.add_argument('--output',
                        dest='output',
                        default='heatmap.png',
                        help='heatmap name (default: heatmap.png)')
    parser.add_argument('--zoom',
                        dest='zoom',
                        type=int,
                        default=13,
                        help='heatmap zoom level 0-19 (default: 13)')

    args = parser.parse_args()

    main(args)