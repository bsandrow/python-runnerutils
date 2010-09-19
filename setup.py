from setuptools import setup, find_packages

setup(
    name            = 'RunnerUtils',
    version         = '0.1',
    packages        = ['lib/runnerutil'],
    scripts         = ['scripts/pyrun'],
    author          = "Brandon Sandrowicz",
    author_email    = "brandon@sandrowicz.org",
    description     = "A package for creating python classes to run as scripts",
    license         = "MIT",
    keywords        = "script runner commandline",
    url             = None,
)
