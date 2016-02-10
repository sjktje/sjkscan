import configparser
import os
import subprocess


def run_cmd(args):
    """Run shell command and return its output.

    :param args: list or string of shell command and arguments
    :returns: output of command

    """

    if isinstance(args, list):
        args = ' '.join(args)

    print("Running: {}".format(args))

    try:
        result = subprocess.check_output(
            args,
            stderr=subprocess.STDOUT,
            shell=True)
    except OSError as e:
        print('Execution failed: {}'.format(e))

    return result


def read_conf(config_file=None):
    """Read and return config.

    The following files will be tried (in order):
        - sjkscan.conf (current directory)
        - ~/.sjkscan.conf
        - /etc/sjkscan/sjkscan.conf
        - /usr/local/etc/sjkscan/sjkscan.conf

    :param string config_file: optional filename to read, defaults to above configs otherwise.
    :returns: dict containing subdicts named after config file sections. Example: dict['Paths']['data'].

    """
    conf = configparser.ConfigParser()

    if config_file:
        conf.read(config_file)
    else:
        conf.read([
            'sjkscan.conf',
            os.path.expanduser('~/.sjkscan.conf'),
            '/etc/sjkscan/sjkscan.conf',
            '/usr/local/etc/sjkscan/sjkscan.conf'
        ])

    out = dict()
    out['Paths'] = dict()
    out['OCR'] = dict()
    out['Rotation'] = dict()

    out['Paths']['data'] = conf['Paths'].get('data', '/Users/sjk/Code/sjkscan/data')
    out['Paths']['dir_format'] = conf['Paths'].get('dir_format', '%Y-%m-%d_%H-%M-%S')
    out['Paths']['inbox'] = conf['Paths'].get('inbox', '%(data)s/INBOX')
    out['Paths']['merged'] = conf['Paths'].get('merged', '%(data)s/merged')

    out['OCR']['language'] = conf['OCR'].get('language', 'swe')

    out['Rotation']['rotate'] = conf['Rotation'].get('rotate', '180')

    return out
