from audio_player import audio_file
from audio_player.lib.audio_file.base_object import AudioFile

from quicktest import TestList
from typing import Type

audio_file_tests = TestList('AudioSource tests.')


def add_tests(adapter_type: Type[AudioFile]):
    @audio_file_tests.test(adapter_type.__name__)
    def test_load_files():
        pass
        # print(adapter_type)


for adapter_type in audio_file.adapter_registry.adapters:
    add_tests(adapter_type)

audio_file_tests.run()
