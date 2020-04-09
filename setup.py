from pip._internal.req import parse_requirements
from setuptools import setup

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]

setup(name="read_rpi", install_requires=load_requirements("requirements.txt"))