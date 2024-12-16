from pathlib import Path
from setuptools import find_packages, setup


THIS_FILE = Path(__file__)


def load_version() -> str:
    version: dict[str, str] = {}
    exec((THIS_FILE.parent / 'src/multiserialviewer/__version__.py').read_text(), version)
    assert version['__version__'], version
    return version['__version__']


def load_req() -> list[str]:
    lines = THIS_FILE.with_name('requirements.txt').read_text().splitlines()
    print(lines)
    return lines


__version__ = load_version()

readme = THIS_FILE.with_name('README.md')
long_description = ''
if readme.is_file():
    with readme.open('r', encoding='utf-8') as fh:
        long_description = fh.read()

setup(
    name='multiserialviewer',
    version=__version__,
    author='shaag',
    description='Shows multiple serial text streams in a single window with individual highlighting options.',
    keywords=[
        'serial',
        'debug output',
        'UART',
        'MCU'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Terminals :: Serial',
        'Topic :: Utilities'
    ],
    url='https://github.com/shaag7967/multiserialviewer',
    project_urls={
        'GitHub': 'https://github.com/shaag7967/multiserialviewer',
    },
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={'multiserialviewer': ['ui_files/*.ui']},
    install_requires=load_req(),
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'multiserialviewer = multiserialviewer.__main__:main'
        ]
    },
    include_package_data=True,
    zip_safe=False
)
