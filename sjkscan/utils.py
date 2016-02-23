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
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            shell=True).stdout
    except OSError as e:
        print('Execution failed: {}'.format(e))

    return result


def files(dir, ext=None):
    """Yield regular files in directory, optionally of specific extension.

    This function is a generator, and could be used like:

        for f in utils.files('/some/directory', 'pnm'):
            do_something_to_the_pnm(f)

    :param dir: directory to traverse
    :param ext: extension of files to list. Leading dot is ignored.

    """

    for f in os.scandir(dir):
        if not f.is_file():
            continue
        if ext and not f.name.endswith('.{}'.format(ext.lstrip('.'))):
            continue
        yield f.name
