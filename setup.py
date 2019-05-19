from setuptools import setup, find_packages

setup(
    name='audio-player',
    version='0.2.5',
    packages=find_packages(),
    url='https://github.com/0xf0f/audio-player',
    license='MIT',
    author='0xf0f',
    author_email='',
    description='audio playback module for python',

    install_requires=[
        'numpy',
        'numba',
        'soundfile',
        'sounddevice',
        'samplerate',
        'cached_property'
        # 'pymediainfo',
    ]
)
