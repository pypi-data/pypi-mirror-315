from setuptools import setup, find_packages

DESCRIPTION = 'Conflux base32 address'


extras_require = {
    'tester': [
        "pytest>=8,<9",
    ],
    'linter': [
        # "black>=22.1.0,<23.0",
        # "flake8==3.8.3",
        # "isort>=4.2.15,<4.3.5",
        # "mypy==0.910",
        # "types-setuptools>=57.4.4,<58",
        # "types-requests>=2.26.1,<3",
        # "types-protobuf==3.19.13",
    ],
    'docs': [
        # "mock",
        # "sphinx-better-theme>=0.1.4",
        # "click>=5.1",
        # "configparser==3.5.0",
        # "contextlib2>=0.5.4",
        # "py-geth>=3.8.0,<4",
        # "py-solc>=0.4.0",
        # "pytest>=6.2.5,<7",
        "sphinx<8",
        "sphinx_rtd_theme>=2.0.0,<3",
        # "toposort>=1.4",
        # "towncrier==18.5.0",
        # "urllib3",
        # "wheel"
    ],
    'dev': [
        # "bumpversion",
        "wheel",
        "pycryptodome",
        "bumpversion==0.6.0"
        # "flaky>=3.7.0,<4",
        # "hypothesis>=3.31.2,<6",
        # "pytest>=6.2.5,<7",
        # "pytest-asyncio>=0.18.1,<0.19",
        # "pytest-mock>=1.10,<2",
        # "pytest-pythonpath>=0.3",
        # "pytest-watch>=4.2,<5",
        # "pytest-xdist>=1.29,<2",
        # "setuptools>=38.6.0",
        # "tox>=1.8.0",
        # "tqdm>4.32,<5",
        # "twine>=1.13,<2",
        # "pluggy==0.13.1",
        # "when-changed>=0.3.0,<0.4"
    ]
}

extras_require['dev'] = (
    extras_require['tester'] # type: ignore
    + extras_require['linter']
    + extras_require['docs']
    + extras_require['dev']
)

with open('./README.md') as readme:
    long_description = readme.read()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="cfx-address",
    version="1.2.4", # edit using bumpversion
    author="The Conflux foundation",
    author_email="wenda.zhang@confluxnetwork.org",
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    python_requires='>=3.7',
    package_data={'cfx_address': ['py.typed']},
    install_requires=[
        "eth-utils>=1.9.5",
        "hexbytes",
        "cfx-utils>=1.0.2",
        "typing_extensions",
        "cached_property==1.5.2;python_version<'3.8'",
        "pydantic>=2.0.0,<3"
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    extras_require=extras_require,
    keywords=['Conflux', 'base32', 'address'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
