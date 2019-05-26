- ~~Modify the audioread module to allow seeking, return floats~~.
  - ~~FFMPEG decoder seems tricky in particular.~~

- Output waveform data from AudioPlayer
	- For things like rendering visualizations.
	
- Add the ability to play multiple files in a playlist

- Mono panning.
	- Numba doesnt support `numpy.repeat` yet so channel duplication
	will have to happen somewhere before the processing pipeline.
	- Perhaps all files could output stereo at a common samplerate and be
	resampled? Would certainly make handling processing pipelines easier
	and would only require one stream per player.

- Add waiting methods to AudioPlayer and AudioPlayerProcessInterface

- Replace placeholder seekbar for large files with realtime waveform visualization

- ~~MIDI file support.~~

- Ability to select soundfont/Timidity config file.
	- Will require adapters to receive a reference to the AudioPlayer instance in their
	`__init__` methods.
	- Can use tempfs to store the temporary config files.

- Playing files from URLs. FFMPEG supports this, but things like looping will require a
	buffering mechanism. i.e. buffer first/last 10-30 seconds of file, stream rest.
	
- Ability to play in reverse.
	- FFMPEG cant do fast seeking when reversed.
	- Soundfile

- SoX pipeline.
	- Also look for other processing modules. PYO seems interesting but unfortunately
	doesnt support past 3.6.
	- Doesn't seem to be any way to make it work synchronously. Have to find a way
	to transmit samplerate/channel dare per block. Also a way to switch/change the
	SoX process at any time.

- Fast adapter selection - A dict mapping extensions to adapters.
	- If extension is not in map then it defaults back to slow selection,
	runs through all the adapters to find one that works.
	
- Better, more granular error handling and reporting.

- A-B looping. Use buffers?

- Decouple AudioFile and decoders.

- Automatically update duration/sample count of files if (during playback) they exceed/fall short of what is reported by AudioInfo.