import argparse

def cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phalanx Generator CLI")
    parser.add_argument('--debug', '-d', action='store_true',
                        help="Enable debugging output")
    parser.add_argument('--loglevel', '--log-level', '-l', default='info',
                        help="Log level (standard logging level names)")
    parser.add_argument('--phalanx-root', '-r',
                        help="Path to root of phalanx directory")
    parser.add_argument('--dry-run', '-x', action='store_true',
                        help="Dry run (output to stdout)")
    return parser.parse_args()

