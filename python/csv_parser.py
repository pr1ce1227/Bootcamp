import argparse

parser = argparse.ArgumentParser(
    prog="csv_parser.py",
    description="Process CSV file",
    epilog="with enough time and practice you will figure it out",
)

parser.add_argument('csv_file', help="CSV file to be parsed")
parser.add_argument('-c', '--column', metavar='COLUMN', nargs='+', type=int, help="columns to select from CSV file")
parser.add_argument('-v', '--verbose', action='store_true',  help="print logging messages")
args = parser.parse_args()




with open(args.csv_file, 'r') as file:
    for line in file:
        data = line.strip().split(',')
        print()
        for index, value in enumerate(data):
                    if index in args.column:
                        print(value, end="")



