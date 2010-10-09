from setuptools import setup, find_packages

setup(
    name            = 'runnerutils',
    version         = '0.1',
    packages        = ['runnerutils'],
    scripts         = ['scripts/runpy'],
    author          = "Brandon Sandrowicz",
    author_email    = "brandon@sandrowicz.org",
    description     = "A package for creating python classes to run as scripts",
    license         = "MIT",
    keywords        = "script runner commandline",
    url             = None,
)
