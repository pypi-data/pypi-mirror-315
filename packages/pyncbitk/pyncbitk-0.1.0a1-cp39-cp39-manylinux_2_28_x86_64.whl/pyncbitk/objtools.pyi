from os import PathLike
from typing import BinaryIO, Iterator, List, Mapping, Union, Optional, Sequence, Sized, Type, KeysView, ValuesView

from .objects.seq import BioSeq
from .objects.seqid import SeqId
from .objects.seqalign import DenseSegments

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore

Molecule = Literal["dna", "rna", "protein", "nucleotide", "other"]
Topology = Literal["linear", "circular", "tandem", "other"]
DatabaseType = Literal["nucleotide", "protein"]
DatabaseVersion = Literal[4, 5]
Strand = Literal[1, -1]

class FastaReader(Iterator[BioSeq]):
    def __init__(self, path: Union[PathLike[str], BinaryIO], *, split: bool = True): ...
    def __iter__(self) -> FastaReader: ...
    def __next__(self) -> BioSeq: ...
    def read(self) -> Optional[BioSeq]: ...

class DatabaseKeysIter(Iterator[SeqId], Sized):
    def __init__(self, db: DatabaseReader) -> None: ...
    def __iter__(self) -> DatabaseKeysIter: ...
    def __len__(self) -> int: ...
    def __next__(self) -> SeqId: ...

class DatabaseValuesIter(Iterator[BioSeq], Sized):
    def __init__(self, db: DatabaseReader) -> None: ...
    def __iter__(self) -> DatabaseValuesIter: ...
    def __len__(self) -> int: ...
    def __next__(self) -> BioSeq: ...

class DatabaseKeys(KeysView[SeqId]):
    def __init__(self, db: DatabaseReader) -> None: ...
    def __iter__(self) -> DatabaseKeysIter: ...
    def __len__(self) -> int: ...
    def __contains__(self, item: object) -> bool: ...

class DatabaseValues(ValuesView[BioSeq]):
    def __init__(self, db: DatabaseReader) -> None: ...
    def __iter__(self) -> DatabaseValuesIter: ...
    def __len__(self) -> int: ...
    def __contains__(self, item: object) -> bool: ...

class DatabaseReader(Mapping[SeqId, BioSeq]):
    def __init__(
        self, name: PathLike[str], type: Optional[DatabaseType] = None
    ) -> None: ...
    def __iter__(self) -> DatabaseKeysIter: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: SeqId) -> BioSeq: ...
    @property
    def version(self) -> DatabaseVersion: ...
    def keys(self) -> DatabaseKeys: ...
    def values(self) -> DatabaseValues: ...

class DatabaseWriter:
    def __init__(
        self,
        name: PathLike[str],
        type: DatabaseType = "nucleotide",
        *,
        title: Optional[str] = None,
        version: int = 4,
    ) -> None: ...
    def __enter__(self) -> DatabaseWriter: ...
    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback,
    ) -> None: ...
    @property
    def volumes(self) -> List[str]: ...
    @property
    def files(self) -> List[str]: ...
    def append(self, sequence: BioSeq) -> None: ...
    def close(self) -> None: ...

class AlignMap(Sequence[AlignMapRow]):
    def __init__(self, segments: DenseSegments) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> AlignMapRow: ...
    @property
    def segments(self) -> DenseSegments: ...

class AlignMapRow:
    @property
    def map(self) -> AlignMap: ...
    @property
    def align_start(self) -> int: ...
    @property
    def align_stop(self) -> int: ...
    @property
    def sequence_start(self) -> int: ...
    @property
    def sequence_stop(self) -> int: ...
    @property
    def strand(self) -> Strand: ...