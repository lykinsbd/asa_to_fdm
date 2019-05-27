from setuptools import setup
from asa_to_fdm import __version__

# We have moved most of the setup arguments over to setup.cfg. Here is the justification for the remaining args:
#   name: necessary for python to understand this package
#   setup_requires: Since we use a setup.cfg file now, the client system needs a version of setuptools that can parse
#        the new file format to get the rest of the metadata.
#   test_suite: Setuptools does not yet support keeping this directive in setup.cfg
#   version: necessary for pip, etc. to tell whether this package meets its requirements. For example, if you want
#        to install "asa_to_fdm>=2.3", is this package even worth downloading?

setup(
    name="asa_to_fdm",
    setup_requires=["setuptools>=30.3"],
    test_suite="asa_to_fdm.tests",
    version=__version__,
)
