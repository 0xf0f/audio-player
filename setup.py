from setuptools import setup, find_packages

setup(
    name='audio-player',
    version='190531.0',
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

    # version_config={
    #     "version_format": "{tag}.dev{sha}",
    #     "starting_version": "0.1.0"
    # },

    # setup_requires=['better-setuptools-git-version'],

    include_package_data=True,
)
