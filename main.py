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
    _color = args.color

    #Download n activities from strava to specified location
    activities_to_consider = strex.export(int(_count), _dir)

    #call heatmap generator to produce png
    hmg.generate_heatmap(activities_to_consider, _dir, _bounds, _output, _zoom, _color)

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
                        default='output/heatmap.png',
                        help='heatmap name (default: output/heatmap.png)')
    parser.add_argument('--zoom',
                        dest='zoom',
                        type=int,
                        default=13,
                        help='heatmap zoom level 0-19 (default: 13)')

    parser.add_argument('--color',
                        dest='color',
                        default='hot',
                        help='matplotlib color map (from https://matplotlib.org/examples/color/colormaps_reference.html)')

    args = parser.parse_args()

    main(args)