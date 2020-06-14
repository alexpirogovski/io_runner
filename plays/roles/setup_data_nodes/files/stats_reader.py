#!/usr/bin/env python

import sys
import subprocess

class StatsReader(object):
    def __init__(self):
        self.stats = {}
        self._cmd = '/home/iguazio//igz/engine/node_runner/bin/stats_reader -f /dev/shm'
        self.raw_stats = self.run_cmd(self._cmd)

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

    # def build_stats_dict(self, raw_output):
    #     return ''

