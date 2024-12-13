import sys
import requests
import setuptools

global tag;
tag:str = None;

global local;
local: bool = False;

if '-tag' in sys.argv:

    tag = sys.argv[ \
        sys.argv.index( '-tag' ) + 1
    ];

else:

    local = True;

def check_version( teg: int ) -> bool:

    '''Return whatever the given tag version is newer than the last release in pyp'''

    global local;
    if local:

        return True;

    response: requests.Response = requests.get( "https://pypi.org/pypi/mikk/json" );

    if response.ok:

        data = response.json();

        versions = list( data[ 'releases' ].keys() )

        latest_version = float( versions[ len( versions ) - 1 ] )

        if float(tag) > latest_version:

            return True;

        raise FileExistsError( f'Version can NOT update {tag}, a newer version already exists ({latest_version})' );

    return False;

if not check_version( tag ):
    exit(0);

setuptools.setup(
    name="mikk",
    version='0.1' if local else tag,
    author="Mikk155",
    author_email="",
    description="Various utilities",
    long_description="Various utilities i do use on various of my projects",
    long_description_content_type="text/markdown",
    url="https://github.com/Mikk155/mikk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        "requests"
    ],
)
