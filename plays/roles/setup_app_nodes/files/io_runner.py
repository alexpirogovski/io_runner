#!/usr/bin/env python

import sys
import json
import logger
import subprocess


class IoRunner(object):
    def __init__(self):
        self.runner = ''

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

    def get_webapi_ip(self):
        cmd = 'kubectl -n default-tenant -o json get svc v3io-webapi'
        try:
            return json.load(IoRunner.run_cmd(cmd))['spec']['clusterIP']
        except json.JSONDecodeError as e:
            print(e.colno)
            return None


def main():
    my_runner = IoRunner()
    # my_runner.get_cache_size()


if __name__ == '__main__':
    main()

