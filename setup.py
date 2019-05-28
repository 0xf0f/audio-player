from setuptools import setup, find_packages

setup(
    name='audio-player',
    version='0.3',
    packages=find_packages(),
    url='https://github.com/0xf0f/audio-player',
    license='MIT',
    author='0xf0f',
    author_email='',
    description='audio playback module for python',

    install_requires=[
        'mido',
        # 'numba',
        'numpy',
        'soundfile',
        'sounddevice',
        'samplerate',
        'cached_property'
        # 'pymediainfo',
    ],

    include_package_data=True,
)
