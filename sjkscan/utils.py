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