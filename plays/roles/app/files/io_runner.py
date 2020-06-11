#!/usr/bin/env python

import sys
import json
import logger
import subprocess


class IoRunner(object):
    def __init__(self):
        # self.node_config = self.get_node_config()
        self.get_cache_size_in_bytes = self.get_cache_size()
        self.webapi_ip = self.get_webapi_ip()

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
    def get_node_config():
        node_config_path = 'node_config.json'
        try:
            with open(node_config_path, 'r') as node_config:
                return json.load(node_config)
        except OSError as e:
            print('Cannot open node_config.json')
            return None

    def get_cache_size(self):
        cache_size_in_bytes = 0
        for p in self.node_config['node']['processes']:
            if 'vn' in p['name']:
                for s in p['services']:
                    cache_size_in_bytes += int(s['emd']['pool_page_nr'])
        cache_size_in_bytes = cache_size_in_bytes * 8 * 1024
        return cache_size_in_bytes

    def get_webapi_ip(self):
        cmd = 'kubectl -n default-tenant -o json get svc v3io-webapi'
        try:
            return json.load(IoRunner.run_cmd(cmd))['spec']['clusterIP']
        except json.JSONDecodeError as e:
            print(e.colno)
            return None


def main():
    my_runner = IoRunner()
    my_runner.get_cache_size()


if __name__ == '__main__':
    main()

