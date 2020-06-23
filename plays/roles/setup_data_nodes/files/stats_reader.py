#!/usr/bin/env python

import sys
import json
import argparse

class StatsReader(object):
    def __init__(self, stats_file):
        with open(stats_file, 'r') as f:
            self.stats = json.load(f)
        self.combined_stats_dict = {
                                        'cache_hits': 0,
                                        'cache_miss': 0,
                                        'cache_d_reads': 0,
                                        'cache_io_pages': 0,
                                        'cache_d_saves': 0
                                   }

    def aggregate_stats(self):
        for key in self.stats.keys():
            if 'cache' in key:
                for cache_key in self.stats[key]:
                    # print(self.stats[key][cache_key]['counts'])
                    self.combined_stats_dict[cache_key] += self.stats[key][cache_key]['counts']

    def print_combined_stats(self):
        print(json.dumps(self.combined_stats_dict, indent=4))

def _parse_cli():
    parser = argparse.ArgumentParser(description='Feed file name to script')
    parser.add_argument('-f', '--file', help='Stats_reader results JSON', required=True)
    return parser.parse_args()

def main():
    args = _parse_cli()
    print('Combined results for {0}'.format(args.file))
    reader = StatsReader(args.file)
    reader.aggregate_stats()
    reader.print_combined_stats()


if __name__ == '__main__':
    sys.exit(main())



