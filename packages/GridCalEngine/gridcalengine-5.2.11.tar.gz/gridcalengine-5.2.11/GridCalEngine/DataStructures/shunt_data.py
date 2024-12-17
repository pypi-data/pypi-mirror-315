# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.  
# SPDX-License-Identifier: MPL-2.0
from typing import Tuple
import numpy as np
import scipy.sparse as sp
import GridCalEngine.Topology.topology as tp
from GridCalEngine.Utils.Sparse.sparse_array import SparseObjectArray
from GridCalEngine.basic_structures import Vec, CxVec, IntVec, StrVec, BoolVec


class ShuntData:
    """
    ShuntData
    """

    def __init__(self, nelm: int, nbus: int):
        """
        Shunt data arrays
        :param nelm: number of shunts
        :param nbus: number of buses
        """
        self.nelm: int = nelm
        self.nbus: int = nbus

        self.names: StrVec = np.empty(nelm, dtype=object)
        self.idtag: StrVec = np.empty(nelm, dtype=object)

        self.active: IntVec = np.zeros(nelm, dtype=bool)

        self.controllable: BoolVec = np.zeros(nelm, dtype=bool)

        self.Y: CxVec = np.zeros(nelm, dtype=complex)

        self.qmin: Vec = np.zeros(nelm, dtype=float)
        self.qmax: Vec = np.zeros(nelm, dtype=float)
        self.q_share: Vec = np.zeros(nelm, dtype=float)

        self.cost: Vec = np.zeros(nelm, dtype=float)

        self.taps = SparseObjectArray(n=self.nelm)

        # reliability
        self.mttf: Vec = np.zeros(nelm, dtype=float)
        self.mttr: Vec = np.zeros(nelm, dtype=float)

        self.C_bus_elm: sp.lil_matrix = sp.lil_matrix((nbus, nelm), dtype=int)

        self.original_idx: IntVec = np.zeros(nelm, dtype=int)

    def size(self) -> int:
        """
        Get size of the structure
        :return:
        """

        return self.nelm

    def slice(self, elm_idx: IntVec, bus_idx: IntVec) -> "ShuntData":
        """
        Slice shunt data by given indices
        :param elm_idx: array of branch indices
        :param bus_idx: array of bus indices
        :return: new ShuntData instance
        """

        data = ShuntData(nelm=len(elm_idx), nbus=len(bus_idx))

        data.names = self.names[elm_idx]
        data.idtag = self.idtag[elm_idx]

        data.active = self.active[elm_idx]

        data.controllable = self.controllable[elm_idx]

        data.Y = self.Y[elm_idx]

        data.qmax = self.qmax[elm_idx]
        data.qmin = self.qmin[elm_idx]
        data.q_share = self.q_share[elm_idx]

        data.cost = self.cost[elm_idx]

        data.taps = self.taps.slice(elm_idx)

        data.mttf = self.mttf[elm_idx]
        data.mttr = self.mttr[elm_idx]

        data.C_bus_elm = self.C_bus_elm[np.ix_(bus_idx, elm_idx)]

        data.original_idx = elm_idx

        return data

    def copy(self) -> "ShuntData":
        """
        Get deep copy of this structure
        :return: new ShuntData instance
        """

        data = ShuntData(nelm=self.nelm, nbus=self.nbus)

        data.names = self.names.copy()
        data.idtag = self.idtag.copy()
        data.active = self.active.copy()
        data.controllable = self.controllable.copy()

        data.Y = self.Y.copy()

        data.qmax = self.qmax.copy()
        data.qmin = self.qmin.copy()
        data.q_share = self.q_share.copy()

        data.cost = self.cost.copy()

        data.taps = self.taps.copy()

        data.mttf = self.mttf.copy()
        data.mttr = self.mttr.copy()

        data.C_bus_elm = self.C_bus_elm.copy()

        data.original_idx = self.original_idx.copy()

        return data

    def get_island(self, bus_idx: IntVec):
        """
        Get the array of shunt indices that belong to the islands given by the bus indices
        :param bus_idx: array of bus indices
        :return: array of island branch indices
        """
        if self.nelm:
            return tp.get_elements_of_the_island(C_element_bus=self.C_bus_elm.T,
                                                 island=bus_idx,
                                                 active=self.active)
        else:
            return np.zeros(0, dtype=int)

    def get_array_per_bus(self, arr: Vec) -> Vec:
        """
        Get generator array per bus
        :param arr:
        :return:
        """
        assert len(arr) == self.nelm
        return self.C_bus_elm @ arr

    def get_injections_per_bus(self) -> CxVec:
        """
        Get Injections per bus
        :return:
        """
        return self.C_bus_elm * (self.Y * self.active)

    def get_fix_injections_per_bus(self) -> CxVec:
        """
        Get fixed Injections per bus
        :return:
        """
        return self.C_bus_elm * (self.Y * self.active * (1 - self.controllable))

    def get_qmax_per_bus(self) -> Vec:
        """
        Get generator Qmax per bus
        :return:
        """
        return self.C_bus_elm * (self.qmax * self.active)

    def get_qmin_per_bus(self) -> Vec:
        """
        Get generator Qmin per bus
        :return:
        """
        return self.C_bus_elm * (self.qmin * self.active)

    def __len__(self) -> int:
        return self.nelm

    def get_bus_indices(self) -> IntVec:
        """
        Get the bus indices
        :return: array with the bus indices
        """
        return tp.get_csr_bus_indices(self.C_bus_elm.tocsr())

    def get_controllable_and_not_controllable_indices(self) -> Tuple[IntVec, IntVec]:
        """
        Get the indices of controllable generators
        :return: idx_controllable, idx_non_controllable
        """
        return np.where(self.controllable == 1)[0], np.where(self.controllable == 0)[0]
