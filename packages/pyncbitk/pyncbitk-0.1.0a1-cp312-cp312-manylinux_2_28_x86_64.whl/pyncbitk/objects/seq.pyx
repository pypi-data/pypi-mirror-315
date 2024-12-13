# cython: language_level=3
"""Biological sequences.

The NCBI C++ Toolkit defines a data model which allows to define biological
sequences as a combination of identifiers that apply to an instance. 
Identifiers are used to identify each sequence uniquely, while the sequence
instance describes the knowledge about that sequence: its molecule type,
length, or actual contents.

See Also:
    The `Biological Sequences <https://ncbi.github.io/cxx-toolkit/pages/ch_datamod#ch_datamod._Biological_Sequences>`_
    section of the NCBI C++ Toolkit documentation.

"""

from libcpp.list cimport list as cpplist

from ..toolkit.corelib.ncbiobj cimport CRef
from ..toolkit.objects.seq.bioseq cimport CBioseq
from ..toolkit.objects.seq.seq_inst cimport CSeq_inst
from ..toolkit.objects.seqloc.seq_id cimport CSeq_id
from ..toolkit.serial.serialbase cimport CSerialObject

from ..serial cimport Serial
from .seqinst cimport SeqInst
from .seqid cimport SeqId, LocalId

import functools

# --- BioSeq -------------------------------------------------------------------

cdef class BioSeq(Serial):
    """A biological sequence.
    """

    @staticmethod
    cdef BioSeq _wrap(CRef[CBioseq] ref):
        cdef BioSeq obj = BioSeq.__new__(BioSeq)
        obj._ref = ref
        return obj

    cdef CSerialObject* _serial(self):
        return <CSerialObject*> self._ref.GetNonNullPointer()

    def __init__(
        self,
        SeqInst instance not None,
        SeqId id,
        *ids,
    ):
        """__init__(self, instance, id, *ids)\n--\n

        Create a new sequence with the given instance and identifiers.

        """
        cdef SeqId    id_
        cdef CBioseq* obj = new CBioseq()

        obj.SetInst(instance._ref.GetObject())
        obj.SetId().push_back(id._ref)
        for id_ in ids:
            obj.SetId().push_back(id_._ref)

        self._ref.Reset(obj)

    def __reduce__(self):
        return functools.partial(type(self), self.instance, *self.ids), ()

    def __repr__(self):
        cdef str ty = self.__class__.__name__
        return f"{ty}({self.instance!r}, {', '.join(repr(id_) for id_ in self.ids)})"

    @property
    def id(self):
        """`~pyncbitk.objects.seqloc.SeqId`: The first sequence identifier.
        """
        assert self._ref.GetNonNullPointer().IsSetId()  # mandatory

        cdef cpplist[CRef[CSeq_id]] _ids  = self._ref.GetNonNullPointer().GetId()
        return SeqId._wrap(_ids.front())

    @property
    def ids(self):
        """`list` of `~pyncbitk.objects.seqloc.SeqId`: The sequence identifiers.
        """
        assert self._ref.GetNonNullPointer().IsSetId()  # mandatory

        cdef SeqId                  seqid
        cdef list                   ids   = []
        cdef cpplist[CRef[CSeq_id]] _ids  = self._ref.GetNonNullPointer().GetId()

        for ref in _ids:
            ids.append(SeqId._wrap(ref))

        return ids

    @property
    def instance(self):
        """`~pyncbitk.objects.seqinst.SeqInst`: The sequence instance.
        """
        assert self._ref.GetNonNullPointer().IsSetInst()  # mandatory
        return SeqInst._wrap(CRef[CSeq_inst](&self._ref.GetNonNullPointer().GetInstMut()))
