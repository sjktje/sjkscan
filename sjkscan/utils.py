import configparser
import os
import subprocess

config = dict()


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


def read_config(config_file=None):
    """Read and populate utils.config

    The following files will be tried (in order):
        - sjkscan.conf (current directory)
        - ~/.sjkscan.conf
        - /etc/sjkscan/sjkscan.conf
        - /usr/local/etc/sjkscan/sjkscan.conf

    Config values can be accessed from within other modules:

        from utils import config
        print(config['Paths'].get('data'))

    given that read_conf() has been called sometime before.

    :param string config_file: optional filename to read, defaults to above configs otherwise.
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

    config['Paths'] = dict()
    config['OCR'] = dict()
    config['Rotation'] = dict()
    config['Scanimage'] = dict()

    config['Paths']['data'] = conf['Paths'].get('data', '/Users/sjk/Code/sjkscan/data')
    config['Paths']['dir_format'] = conf['Paths'].get('dir_format', '%Y-%m-%d_%H-%M-%S')
    config['Paths']['inbox'] = conf['Paths'].get('inbox', '%(data)s/INBOX')
    config['Paths']['merged'] = conf['Paths'].get('merged', '%(data)s/merged')

    config['OCR']['language'] = conf['OCR'].get('language', 'swe')

    config['Rotation']['rotate'] = conf['Rotation'].get('rotate', '180')

    config['Scanimage']['resolution'] = conf['Scanimage'].get('resolution', 300)
    config['Scanimage']['brightness'] = conf['Scanimage'].get('brightness', 80)
    config['Scanimage']['contrast'] = conf['Scanimage'].get('contrast', 100)
