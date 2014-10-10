#!/usr/bin/env python

from maas_common import metric, status_err, status_ok
import shlex
import subprocess

def utilisation(time):
    output = subprocess.check_output(shlex.split('iostat -x -d %s 2' % time))
    device_lines = output.split('\nDevice:')[-1].strip().split('\n')[1:]
    devices = [d for d in device_lines if not d.startswith('dm-')]
    devices = [d.split() for d in devices]
    utils = [(d[0], d[-1]) for d in devices]
    return utils


def main():
    try:
        utils = utilisation(5)
    except Exception as e:
        status_err(e)
    else:
        status_ok()
        for util in utils:
            metric('disk_utilisation_%s' % util[0], 'double', util[1], '%')


if __name__ == '__main__':
    main()
