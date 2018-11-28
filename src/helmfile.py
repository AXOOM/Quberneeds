from os import environ
from external_tool import run

def charts(environment, helmfilePath, helmArgs=None):
    args = ['helmfile','-f', helmfilePath, 'charts']
    if helmArgs:
        args += ['--args', helmArgs]

    apply_environ(environment)
    run(*args)


def delete(environment, helmfilePath, purge=False):
    args = ['helmfile', '-f', helmfilePath, 'delete']
    if purge:
        args += ['--purge']

    apply_environ(environment)
    run(*args)


def apply_environ(environment):
    for key, value in environment.items():
        if value is None:
            raise TypeError('Unable to set env var %s -- value is None' % (key))
        else:
            environ[key] = value
