import numpy as np
import re
from typing import List


class SampleHandler:
    NEGATIVE_SIGNAL = '-'
    POSITIVE_SIGNAL = 'o'

    def _numeralize_char(self, character: str) -> int:
        character = character.lower()
        return 0 if character == self.NEGATIVE_SIGNAL else 1

    def _numeralize_sample(self, sample: str) -> np.ndarray:
        line_arr_sample = sample.strip().split('\n')
        num_arr_sample = []
        for line in line_arr_sample:
            # TODO code readability or efficiency. one liners?
            num_arr_sample.append(list(map(self._numeralize_char, [ch for ch in line])))
        return np.array(num_arr_sample)

    def _numeralize_samples(self, samples: List[str]) -> List[np.ndarray]:
        return [self._numeralize_sample(sample) for sample in samples]

    def extract_samples(self, content: str) -> List[np.ndarray]:
        # TODO could be 2 steps?
        all_samples = re.findall(r'~{4}(.*?)~{4}', content, re.DOTALL)
        # TODO separator can be an input?
        return self._numeralize_samples(all_samples)


class FileHandler:
    file_path = None

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_file_content(self) -> str:
        file = open(self.file_path, 'r')
        content = file.read()
        file.close()
        return content


class InputFileHandler(FileHandler):
    samples = []

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self._extract_samples()

    def _extract_samples(self):
        content = self.get_file_content()  # TODO will we need content?
        self.samples = SampleHandler().extract_samples(content)

    def get_known_invader_samples(self) -> List[np.ndarray]:
        # TODO depends on file format but is it ok?
        # TODO handle on SampleHandler instead?
        return self.samples[:-1]

    def get_radar_sample(self) -> np.ndarray:
        # TODO depends on file format but is it ok?
        return self.samples[-1]
