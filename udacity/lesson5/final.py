import csv
from pathlib import Path
from os.path import dirname, abspath
import argparse


from udacity.lesson5 import filereader, filewritter

class TripPlanner():
    def __init__(self):
        self.airports = None
        self.airlines = None
        self.routes = None
        self.destiny = None
    
    def load_airports(self, filename):
        self.airports = filereader.read_csv(filename)

    def load_airlines(self, filename='airlines.dat'):
        airlines = {}  
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                airlines[line[4]] = line[1]
        self.airlines = airlines

    def load_routes(self, filename='routes.dat'):
        self.routes = filereader.read_csv(filename)


    def find_routes(self, origin, destiny, max_segments=None):
        if not max_segments:
            max_segments = 1
        if not self.airports:
            self.load_airports()
        if not self.routes:
            self.load_routes()
        self.destiny = destiny
        all_routes = {}
        routes_from_origin = self._get_routes_from_airport(origin)
        for segments in range(1, max_segments+1):
            routes_to_destiny = self._find_destiny(routes_from_origin, segments)
            all_routes[str(segments)] = routes_to_destiny
        return all_routes

    def _get_routes_from_airport(self, airport):
        routes = []
        for route in self.routes:
            if airport in route[2]:
                routes.append([route[2],route[4]])
        return routes

    def _find_destiny2(self, start_routes, segments):
        routes_found = {}
        routes = start_routes
        for segment in range(1, segments+1):
            for route in routes:
                if self.destiny in route[-1] and route not in routes_found:
                    routes_found[str(segment)] = routes_found[str(segment)].append(route)
        return routes_found

    def _find_destiny(self, start_routes, segments):
        routes_found = []
        routes = start_routes
        if segments > 1:
            routes = self._expand_routes(routes, segments)
        for route in routes:
            if self.destiny in route[-1] and route not in routes_found:
                routes_found.append(route)
        return routes_found

    def _expand_routes(self, routes, segments):
        routes_by_segment = routes
        for segment in range(segments-1):
            new_routes = []
            for route in routes_by_segment:
                last_airport = route[-1]
                if last_airport == self.destiny:
                    continue
                next_routes = self._get_routes_from_airport(last_airport)
                for next_route in next_routes:
                    new_route = [*route,next_route[-1]]
                    if new_route not in new_routes:
                        new_routes.append(new_route)
            routes_by_segment = new_routes
        return new_routes
         

def main(source, dest, max_segments):
    repo_path = dirname(dirname(dirname(abspath(__file__))))
    airports = Path(repo_path, "tests/helpers/lesson5/airports.dat")
    routes = Path(repo_path, "tests/helpers/lesson5/routes.dat")
    outfile = Path(repo_path, "tests/helpers/lesson5/output.json")
    planner = TripPlanner()
    planner.load_airports(airports)
    planner.load_routes(routes)
    routes = planner.find_routes(source, dest, max_segments)
    filewritter.write_json(outfile, routes)
    print(routes)
    print(repo_path)
    print(f"Routes saved in file {outfile}")

def build_parser():
    """Create a parser to parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Find flight paths between two airlines")
    parser.add_argument('source', help="The source airport's IATA (3-letter) code.")
    parser.add_argument('dest', help="The destination airport's IATA (3-letter) code.")
    parser.add_argument('--max-segments', dest='max_segments', type=int, default=2,
                        help="The maximum number of segments in a valid path.")                        
    return parser

if __name__ == "__main__":
    arg_parser = build_parser()
    args = arg_parser.parse_args()
    main(args.source, args.dest, args.max_segments)
    