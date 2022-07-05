from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'html5lib',
    'pathlib',
    'pandas'
    ]

setup(
    name='Flightify',
    version='1.0',
    description='An application that generates a Spotify playlist corresponding to a flight length',
    author='Edwin Chow',
    author_email='edwinchow1110@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)

