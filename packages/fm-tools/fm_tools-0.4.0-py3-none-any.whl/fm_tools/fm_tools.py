from pathlib import Path
from typing import Dict, Iterator

from fm_tools.basic_config import BASE_DIR
from fm_tools.competition_participation import Competition, Track
from fm_tools.fmdata import FmData


class FmTools:
    """
    Entry class parsing all yaml files in a directory and providing access to the data.
    """

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or BASE_DIR
        self.data = self._parse_all_files()

    def _parse_all_files(self) -> Dict[str, FmData]:
        data = {}
        for file in self.base_dir.glob("*.yml"):
            if file.stem == "schema":
                continue
            data[file.stem] = FmData.from_file(file)
        return data

    def get(self, item: str) -> FmData:
        return self.data[item]

    def __getitem__(self, item: str) -> FmData:
        return self.get(item)

    def __getattr__(self, item: str) -> FmData:
        try:
            return self.data[item]
        except KeyError:
            raise AttributeError(f"File {item} not found") from KeyError

    def __iter__(self) -> Iterator[FmData]:
        return iter(self.data.values())

    def __contains__(self, item: str) -> bool:
        return item in self.data

    def query(self, competition: Competition, year: int, track: Track = Track.Any):
        from fm_tools.query import Query

        return Query(self, competition, year, track)
