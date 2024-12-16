import pathlib
import abc


class AbstractParser(abc.ABC):
    """
    Converts aTrain transcripts into a dictionary containing the data for a conversational space map.
    """

    def __init__(self, file: pathlib.Path) -> None:
        self._file = file
        self._content = self._read_file()
        self._map: dict[int: dict] = self._convert_text()

    @property
    def file(self) -> pathlib.Path:
        return self._file

    @property
    def map(self) -> dict[int: dict]:
        return self._map

    @property
    def content(self) -> str:
        return self._content

    @abc.abstractmethod
    def number_of_words_by_speaker(self) -> [int, int]:
        raise NotImplementedError

    def _read_file(self) -> str:
        return self._file.read_text()

    @abc.abstractmethod
    def _convert_text(self) -> dict[int:dict]:
        raise NotImplementedError

    @property
    def map_list(self) -> list[int]:
        """
        Return lists of words by utterance by speaker (only applies for two speakers)
        """
        output = []
        for utterance in self._map.items():
            if utterance[0] % 2 == 1:
                output.append(-utterance[1]["words"])
            else:
                output.append(utterance[1]["words"])
        return output


class TimestampCleanParser(AbstractParser):

    @property
    def number_of_words_by_speaker(self) -> [int, int]:
        return [
            abs(sum(self.map_list[::2])),
            abs(sum(self.map_list[1::2])),
        ]

    def _convert_text(self) -> dict[int:dict]:
        self._content = self._content.replace("\n-", "")
        tokens = self._content.split("\n\n")
        output = {}
        counter = 0
        for token in tokens:
            segments = token.split(" ")
            counter += 1
            output[counter] = {
                "speaker": segments[0],
                "words": len(segments)-1,
            }
        return output
