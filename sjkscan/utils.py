import configparser
import subprocess

from pkg_resources import resource_string


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
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            shell=True).stdout
    except OSError as e:
        print('Execution failed: {}'.format(e))

    return result


def read_config(config_file=None):
    """Read and populate utils.config

    Config values can be accessed from within other modules:

        from utils import config
        print(config['Paths'].get('data'))

    given that read_conf() has been called sometime before.

    :param string config_file: optional filename to read, otherwise looks for sjkscan.conf in bundle.

    """
    conf = configparser.ConfigParser()

    if config_file:
        conf.read(config_file)
    else:
        conf.read_string(resource_string(__name__, 'sjkscan.conf').decode('utf-8'))

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
