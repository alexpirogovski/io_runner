#!/usr/bin/env python

import os
import sys
import json
import subprocess

class DataNodeAgent(object):
    def __init__(self):
        self.node_config = self.get_node_config()
        self.cache_size_bytes = self.get_cache_size_bytes()

    def get_cache_size_bytes(self):
        cache_size_in_bytes = 0
        for p in self.node_config['node']['processes']:
            if 'vn' in p['name']:
                for s in p['services']:
                    cache_size_in_bytes += int(s['emd']['pool_page_nr'])
        cache_size_in_bytes = cache_size_in_bytes * 8 * 1024
        return cache_size_in_bytes

    @staticmethod
    def get_node_config():
        node_config_path = 'node_config.json'
        try:
            with open(node_config_path, 'r') as node_config:
                return json.load(node_config)
        except OSError as e:
            print('Cannot open node_config.json')
            return None

    @staticmethod
    def run_cmd(cmd, exit_on_fail=True):
        try:
            # logger.debug('Executing: {}'.format(cmd))
            return subprocess.check_output(cmd.split(' ')).split('\n')
        except subprocess.CalledProcessError as e:
            # logger.error('Command \"{}\" exited with RC={}, message: {}'.format(cmd, e.returncode, e.output))
            print('ERROR: %s, RC=%s', e.output, e.returncode)
            if exit_on_fail:
                sys.exit(1)
            return None

    @staticmethod
    def set_fact(key, value):
        facts_path = '/etc/ansible/facts.d/'
        fact_file = os.path.join(facts_path, key, '.ini')
        with open(fact_file, 'w') as fact_f:
            line = '='.join([key, value])
            fact_f.writelines(line)