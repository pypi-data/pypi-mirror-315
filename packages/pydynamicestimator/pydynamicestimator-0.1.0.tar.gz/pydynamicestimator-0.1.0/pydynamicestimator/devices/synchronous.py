# Filename: devices/synchronous.py
# Created: 2024-12-01
# Last Modified: 2024-12-04
# (c) Copyright 2024 ETH Zurich, Milos Katanic
# https://doi.org/10.5905/ethz-1007-842
#
# Licensed under the GNU General Public License v3.0;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     https://www.gnu.org/licenses/gpl-3.0.en.html
#
# This software is distributed "AS IS", WITHOUT WARRANTY OF ANY KIND,
# express or implied. See the License for specific language governing
# permissions and limitations under the License.
#

# The code is based on the publication: Katanic, M., Lygeros, J., Hug, G.: Recursive dynamic state estimation for power systems with an incomplete nonlinear DAE model.
# IET Gener. Transm. Distrib. 18, 3657–3668 (2024). https://doi.org/10.1049/gtd2.13308
# The full paper version is available at: https://arxiv.org/abs/2305.10065v2
# See full metadata at: README.md
# For inquiries, contact: mkatanic@ethz.ch


from __future__ import annotations  # Postponed type evaluation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydynamicestimator.system import *
from devices.device import *


class SynchronousTransient(Synchronous):
    """Transient two-axis SG with TGOV1 governor and IEEEDC1A AVR"""

    def __init__(self) -> None:
        super().__init__()

        self._type = "Synchronous_machine"
        self._name = 'Synchronous_machine_transient_model'

        self._states_noise.update(
            {'delta': 1e-2, 'omega': 1e-2, 'ed': 1, 'eq': 1, 'pm1': 1, 'pm': 1, 'Ef': 1, 'Ef1': 1, 'Ef2': 1})
        self._states_init_error.update(
            {'delta': 0.1, 'omega': 0.001, 'ed': 0.1, 'eq': 0.1, 'pm1': 0.1, 'pm': 0.1, 'Ef': 0.1, 'Ef1': 0.1, 'Ef2': 0.1})
        self._x0.update({'delta': 2.14, 'omega': 0.0, 'ed': -0.4, 'eq': 1, 'pm1': 0.5, 'pm': 0.5, 'Ef': 1.5, 'Ef1': 0.0,
                         'Ef2': 1.5})
        self._descr.update({'H': 'inertia constant', 'D': 'rotor damping', 'fn': 'rated frequency', 'bus': 'bus id',
                            'gen': 'static generator id', 'R_s': 'stator resistance',
                            'T_dprim': 'd-axis transient time constant', 'T_qprim': 'q-axis transient time constant',
                            'x_d': 'd-axis synchronous reactance', 'x_dprim': 'd-axis transient reactance',
                            'x_q': 'q-axis synchronous reactance', 'x_qprim': 'q-axis transient reacntance'})
        self.properties.update(
            {'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': True, 'qcall': True, 'gcall': True})

        self._init_data()

    def input_current(self, dae: Dae):
        # differential equations
        i_d = SX.sym('id', self.n)
        i_q = SX.sym('iq', self.n)
        for i in range(self.n):
            adq = SX([[self.R_s[i], self.x_qprim[i]], [-self.x_dprim[i], self.R_s[i]]])
            b1 = +dae.y[self.vre[i]] * sin(dae.x[self.delta[i]]) - dae.y[self.vim[i]] * cos(dae.x[self.delta[i]]) + dae.x[self.ed[i]]
            b2 = -dae.y[self.vre[i]] * cos(dae.x[self.delta[i]]) - dae.y[self.vim[i]] * sin(dae.x[self.delta[i]]) + dae.x[self.eq[i]]
            b = vertcat(b1, b2)
            i_dq = solve(adq, b) * dae.Sb/self.Sn[i]  # scale the current for the base power inside the machine
            i_d[i] = i_dq[0]
            i_q[i] = i_dq[1]
        return i_d, i_q

    def two_axis(self, dae, i_d, i_q):
        dae.f[self.delta] = 2 * np.pi * self.fn * dae.x[self.omega]
        dae.f[self.omega] = 1 / (2 * self.H) * (
                dae.x[self.pm] - dae.x[self.ed] * i_d - dae.x[self.eq] * i_q + (self.x_qprim - self.x_dprim) * i_d * i_q - self.D * dae.x[self.omega] - self.f * (
                dae.x[self.omega] + 1))  # omega
        dae.f[self.eq] = 1 / self.T_dprim * (-dae.x[self.eq] + dae.x[self.Ef] + (self.x_d - self.x_dprim) * i_d)  # Eq
        dae.f[self.ed] = 1 / self.T_qprim * (-dae.x[self.ed] - (self.x_q - self.x_qprim) * i_q)  # Ed

    def fgcall(self, dae: Dae) -> None:
        i_d, i_q = self.input_current(dae)

        self.two_axis(dae, i_d, i_q)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)

    # def init_add(self, dae: Dae):
    #     add = SX.casdadi('', 1)
    #     add[0] = self.Qref - dae.x[self.Qint]


class SynchronousSubtransient(Synchronous):
    """Subtransient SG with TGOV1 governor and IEEEDC1A AVR"""

    def __init__(self) -> None:
        super().__init__()

        # private data
        self._type = "Synchronous_machine"
        self._name = 'Synchronous_machine_subtransient_model'
        self._params.update(
            {'H': 30, 'R_s': 0.0, 'x_d': 0.2, 'x_q': 0.2, 'x_dprim': 0.05, 'x_qprim': 0.1,
             'x_dsec': 0.01, 'x_qsec': 0.01, 'T_dsec': 0.001, 'T_qsec': 0.001,
             'T_dprim': 8.0, 'T_qprim': 0.8, 'D': 0.0, 'R': 0.05, 'T1': 0.05, 'T2': 0.5, 'T3': 1.5,
             'KA': 200.0, 'TA': 0.015, 'KF': 1.0, 'TF': 0.1, 'KE': 1.0, 'TE': 0.04, 'Vref': 1.03,
             'f': 0.01, 'V_exc': 2.0})

        self.states.extend(['ed1', 'eq1'])
        self.ns += 2
        self._states_noise.update(
            {'delta': 1e-2, 'omega': 1e-2, 'ed': 1, 'eq': 1, 'pm1': 1, 'pm': 1, 'Ef': 1, 'Ef1': 1, 'Ef2': 1, 'ed1': 1, 'eq1': 1})
        self._states_init_error.update(
            {'delta': 0.1, 'omega': 0.001, 'ed': 0.1, 'eq': 0.1, 'pm1': 0.1, 'pm': 0.1, 'Ef': 0.1, 'Ef1': 0.1, 'Ef2': 0.1, 'ed1': 0.1, 'eq1': 0.1})
        self._x0.update(
            {'delta': 0.0, 'omega': 0.0, 'ed': 0.0, 'eq': 0.0, 'pm1': 0.5, 'pm': 0.5, 'Ef': 1.3, 'Ef1': 0.0, 'Ef2': 1.3,
             'ed1': 0.0, 'eq1': 0.0})

        self._descr.update({'H': 'inertia constant', 'D': 'rotor damping', 'fn': 'rated frequency', 'bus': 'bus id',
                            'gen': 'static generator id', 'R_s': 'stator resistance',
                            'T_dprim': 'd-axis transient time constant', 'T_qprim': 'q-axis transient time constant',
                            'x_d': 'd-axis synchronous reactance', 'x_dprim': 'd-axis transient reactance',
                            'x_q': 'q-axis synchronous reactance', 'x_qprim': 'q-axis transient reactance'})

        self.properties.update(
            {'fgcall': True, 'finit': True, 'init_data': True, 'xy_index': True, 'save_data': True, 'qcall': True})

        # Parameters
        self.x_dsec = np.array([], dtype=float)
        self.x_qsec = np.array([], dtype=float)
        self.T_dsec = np.array([], dtype=float)
        self.T_qsec = np.array([], dtype=float)

        # States
        self.ed1 = np.array([], dtype=float)
        self.eq1 = np.array([], dtype=float)

        self._init_data()

    def input_current(self, dae: Dae):
        # differential equations
        i_d = SX.sym('Id', self.n)
        i_q = SX.sym('Iq', self.n)
        for i in range(self.n):
            adq = SX([[self.R_s[i], self.x_qsec[i]], [-self.x_dsec[i], self.R_s[i]]])
            b1 = +dae.y[self.vre[i]] * sin(dae.x[self.delta[i]]) - dae.y[self.vim[i]] * cos(dae.x[self.delta[i]]) + dae.x[self.ed1[i]]
            b2 = -dae.y[self.vre[i]] * cos(dae.x[self.delta[i]]) - dae.y[self.vim[i]] * sin(dae.x[self.delta[i]]) + dae.x[self.eq1[i]]
            b = vertcat(b1, b2)
            i_dq = solve(adq, b) * dae.Sb/self.Sn[i]  # scale the current for the base power inside the machine
            i_d[i] = i_dq[0]
            i_q[i] = i_dq[1]
        return i_d, i_q

    def anderson_fouad(self, dae: Dae, i_d: casadi.SX, i_q: casadi.SX):
        dae.f[self.delta] = 2 * np.pi * self.fn * dae.x[self.omega]
        dae.f[self.omega] = 1 / (2 * self.H) * (
                    dae.x[self.pm] - dae.x[self.ed1] * i_d - dae.x[self.eq1] * i_q + (self.x_qsec - self.x_dsec) * i_d * i_q - self.D * dae.x[self.omega] - self.f * (
                        dae.x[self.omega] + 1))  # omega
        dae.f[self.eq] = 1 / self.T_dprim * (-dae.x[self.eq] + dae.x[self.Ef] + (self.x_d - self.x_dprim) * i_d)  # Eq
        dae.f[self.ed] = 1 / self.T_qprim * (-dae.x[self.ed] - (self.x_q - self.x_qprim) * i_q)  # Ed
        dae.f[self.eq1] = 1 / self.T_dsec * (dae.x[self.eq] - dae.x[self.eq1] + (self.x_dprim - self.x_dsec) * i_d)
        dae.f[self.ed1] = 1 / self.T_qsec * (dae.x[self.ed] - dae.x[self.ed1] - (self.x_qprim - self.x_qsec) * i_q)

    def fgcall(self, dae: Dae) -> None:
        i_d, i_q = self.input_current(dae)

        self.anderson_fouad(dae, i_d, i_q)

        self.tgov1(dae)

        self.ieeedc1a(dae)

        self.gcall(dae, i_d, i_q)
