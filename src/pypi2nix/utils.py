import click
import shlex
import subprocess


TO_IGNORE = [
    "setuptools",
    "wheel",
    "zc.buildout",
    "zc.recipe.egg",
]

PYTHON_VERSIONS = {
    "2.6": "python26",
    "2.7": "python27",
    "3.2": "python32",
    "3.3": "python33",
    "3.4": "python34",
    "3.5": "python35",
    "3": "python3",
    "pypy": "pypy",
}


def pretty_option(option):
    if option is None:
        return ''
    else:
        return ' [value: {}]'.format(
            type(option) in [list, tuple]
            and ' '.join(option)
            or option)

def safe(string):
    return string.replace('"', '\\"')


def cmd(command):

    if isinstance(command, str):
        command = shlex.split(command)

    click.echo('|-> ' + ' '.join(command))
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        )

    out = []
    while True:
        line = p.stdout.readline().decode()
        if line == '' and p.poll() is not None:
            break
        if line != '':
            click.echo('    ' + line.rstrip('\n'))
            out.append(line)

    return p.returncode


def create_command_options(options):
    command_options = []
    for name, value in options.items():
        if isinstance(value, str):
            command_options.append('--argstr {} "{}"'.format(name, value))
        elif isinstance(value, list) or isinstance(value, tuple):
            value = "[ %s ]" % (' '.join(['"%s"' % x for x in value]))
            command_options.append("--arg {} '{}'".format(name, value))
    return ' '.join(command_options)
