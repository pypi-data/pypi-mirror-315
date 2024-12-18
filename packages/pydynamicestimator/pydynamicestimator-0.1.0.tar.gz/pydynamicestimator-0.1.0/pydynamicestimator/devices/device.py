# Filename: devices/device.py
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
from typing import Union, Any, Optional

if TYPE_CHECKING:
    from system import Dae, Grid, DaeEst, DaeSim
from casadi import *
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

np.random.seed(30)
sin = np.sin
cos = np.cos
sqrt = np.sqrt


class Element:
    """Metaclass to be used for all elements to be added"""

    def __init__(self) -> None:
        self.n: int = 0  # number of devices
        self.u: list[bool] = []  # device status
        self.name: list[str] = []  # name of the device
        self._type: Optional[str] = None  # Device type
        self._name: Optional[str] = None  # Device name
        self.int: dict[str, Union[str, int]] = {}  # Dictionary of unique identifiers for each device based on the variable "idx"
        self._data: dict[str, Any] = {'u': True}  # Default entries for lists
        self._params: dict[str, float] = {}  # Default entries for np.arrays params
        self._setpoints: dict[str, float] = {}  # Default entries for np.arrays set points
        self._descr: dict[str, str] = {}  # Parameter and data explanation
        self._mand: list[str] = []  # mandatory attributes
        self.properties: dict[str, bool] = {'gcall': False, 'fcall': False, 'xinit': False, 'fgcall': False, 'qcall': False, 'call': False, 'xy_index': False, 'finit': False,
                                            'save_data': False, 'fplot': False}

    def add(self, idx: Optional[str] = None, name: Optional[str] = None, **kwargs) -> None:
        """
        Add am element device

        Args:
        idx (str, optional): Unique identifier for the device. Generated if not provided.
        name (str, optional): Name of the device. Generated if not provided.
        **kwargs: Custom parameters to overwrite defaults.
        """
        # Generate unique identifiers if not provided
        idx = idx or f"{self._type}_{self.n + 1}"
        name = name or f"{self._name}_{self.n + 1}"

        self.int[idx] = self.n
        self.name.append(name)

        # check whether mandatory parameters have been set up

        for key in self._mand:
            if key not in kwargs:
                raise Exception('Mandatory parameter <%s> has not been set up' % key)
        self.n += 1
        # Set default values
        for key, default in {**self._params, **self._setpoints}.items():
            if key not in self.__dict__:
                logger.warning(f"Attribute {key} not found in element - initializing as an empty array.")
                self.__dict__[key] = np.array([], dtype=type(default))
            self.__dict__[key] = np.append(self.__dict__[key], default)

        for key, default in self._data.items():
            if key not in self.__dict__:
                logger.warning(f"Attribute {key} not found in element - initializing as an empty list.")
                self.__dict__[key] = []
            self.__dict__[key].append(default)

        # Overwrite custom values

        for key, value in kwargs.items():

            if key not in self.__dict__:
                logger.warning('Element %s does not have parameter %s - ignoring' % (self._name, key))
                continue
            self.__dict__[key][-1] = value

        logger.info(f"Element {name} (ID: {idx}) added successfully.")


class BusInit(Element):

    def __init__(self) -> None:
        super().__init__()
        self._type = "Bus_init_or_unknwon"  # Element type
        self._name = "Bus_init_or_unknown"  # Element name
        self._data.update({'bus': None, 'p': 0, 'q': 0, 'v': 1.0, 'type': None})
        self.bus: list[Optional[str]] = []
        self.p: list[float] = []
        self.q: list[float] = []
        self.v: list[float] = []
        self.type: list[Optional[str]] = []


BusUnknown = BusInit # Alias class anem


class Disturbance(Element):

    def __init__(self) -> None:
        super().__init__()
        self._type = "Disturbance"  # Element type
        self._name = "Disturbance"  # Element name
        # Default parameter values
        self._params.update({'bus_i': None, 'bus_j': None, 'time': None, 'type': None, 'y': 10, 'bus': None, 'p_delta': 0, 'q_delta': 0})

        self.type = np.array([], dtype=str)
        self.time = np.array([], dtype=float)
        self.bus_i = np.array([], dtype=str)
        self.bus_j = np.array([], dtype=str)
        self.y: np.ndarray = np.array([], dtype=float)
        self.bus = np.array([], dtype=str)
        self.p_delta = np.array([], dtype=float)
        self.q_delta = np.array([], dtype=float)


class Line(Element):

    def __init__(self) -> None:
        super().__init__()

        self._type = "Transmission_line"  # Element type
        self._name = "Transmission_line"  # Element name
        self._params.update({'r': 0.001, 'x': 0.001, 'g': 0, 'b': 0, 'bus_i': None, 'bus_j': None, 'trafo': 1})
        self.r = np.array([], dtype=float)
        self.x = np.array([], dtype=float)
        self.g = np.array([], dtype=float)
        self.b = np.array([], dtype=float)
        self.trafo = np.array([], dtype=float)
        self.bus_i = np.array([], dtype=object)
        self.bus_j = np.array([], dtype=object)


class DeviceRect(Element):
    """
    Dynamic or static device modeled in rectangular coordinates

    Attributes:
        properties (dict[str, bool]): Flags for method calls (e.g., 'gcall', 'fcall').
        xf (dict[str, np.ndarray]): Final state results for simulation/estimation.
        xinit (dict[str, list[float]]): Initial state values.
        _params (dict[str, float]): Device parameters, such as rated voltage, power, and frequency.
        Vn, fn, Sn (np.ndarray): Device-specific rated voltage, frequency, and power.
        bus (list[Optional[str]]): Buses where the device is connected.
        states (list[str]): State variables.
        _algebs (list[str]): Algebraic variables ('vre', 'vim').
        _descr (dict[str, str]): Descriptions for key parameters.
    """

    def __init__(self) -> None:

        super().__init__()

        self.xf: dict[str, np.ndarray] = {}  # final state results or sim/est
        self.xinit: dict[str, list[float]] = {}

        self._params.update({'Vn': 220, 'fn': 50.0, 'Sn': 100})
        self.Vn = np.array([], dtype=float)
        self.fn = np.array([], dtype=float)
        self.Sn = np.array([], dtype=float)

        self._data.update({'bus': None})
        self.bus: list[Optional[str]] = []  # at which bus

        self.states: list[str] = []  # list of state variables
        self.ns: int = 0  # number of states
        self._unknown_inputs: list[str] = []  # list of unknown input variables (only for estimation)
        self._switches: list[str] = []  # list of switches
        self._states_noise: dict[str, float] = {}  # list of noises for every state variable
        self._states_init_error: dict[str, float] = {}  # list of noises for every state variable
        self._algebs: list[str] = ['vre', 'vim']  # list of algebraic variables
        self.vre = np.array([], dtype=float)
        self.vim = np.array([], dtype=float)

        self._x0: dict[str, float] = {}  # default initial states, will be used as initial guess for the simulation initialization
        self._mand.extend(['bus'])
        self._descr = {'Sn': 'rated power', 'Vn': 'rated voltage', 'u': 'connection status', 'fn': 'nominal frequency'}

    def _init_data(self) -> None:

        self.xinit = {state: [] for state in self.states}

    def xy_index(self, dae: Dae, grid: Grid) -> None:

        """Initializes indices for states, algebraic variables, unknown inputs, and switches.

            Args:
                dae (Dae): Object managing differential-algebraic equations.
                grid (Grid): Object managing the electrical grid and node indices.
        """

        zeros = [0] * self.n
        for item in self.states:
            self.__dict__[item] = zeros[:]
        for item in self._algebs:
            self.__dict__[item] = zeros[:]
        for item in self._unknown_inputs:
            self.__dict__[item] = zeros[:]
        for item in self._switches:
            self.__dict__[item] = zeros[:]

        for var in range(self.n):

            for item in self.states:
                self.__dict__[item][var] = dae.nx
                # Init with current state init value
                dae.xinit.append(self.xinit[item][var])
                dae.nx += 1
        if self.n:
            # assign indices to real and imaginary voltage algebraic variables; first real value
            self.__dict__['vre'] = grid.get_node_index(self.bus)[1]
            self.__dict__['vim'] = grid.get_node_index(self.bus)[2]

    def add(self, idx=None, name=None, **kwargs) -> None:

        super().add(idx, name, **kwargs)

        # initialize initial states with some default values
        for item in self.states:
            self.xinit[item].append(self._x0[item])

    def init_from_simulation(self, device_sim: DeviceRect, idx: str, dae: DaeEst, dae_sim: DaeSim) -> None:

        """Initialize the device state estimation based on simulation results.

            Args:
                device_sim (DeviceRect): The device simulation object containing simulation results.
                idx (str): unique index of the device
                dae (DaeEst): The DAE object responsible for managing the estimation of the system.
                dae_sim (DaeSim): The simulation object providing timing information.
        """

        var_sim = device_sim.int.get(idx)
        var_est = self.int.get(idx)

        # Initial states of estimation as true states obtained through simulation
        for item in self.states:
            # Init with simulated value
            try:
                self.xinit[item][var_est] = device_sim.xf[item][var_sim, round(dae.T_start / dae_sim.t)]
            except KeyError:
                logger.error(f"Failed to initialize state {item}. State not found in simulation model.")
                continue
            # Add noise for the init state
            noise = self._states_init_error[item] * (np.random.uniform() - 0.5) * dae.init_error_diff
            dae.xinit[self.__dict__[item][var_est]] = self.xinit[item][var_est] + noise

        # Set setpoint values based on simulation
        for item, value in self._setpoints.items():
            if item in device_sim.__dict__:
                self.__dict__[item][var_est] = device_sim.__dict__[item][var_sim]
            else:
                logger.warning(f"Setpoint {item} not found in simulation data. Skipping. It will be ignored and the estimation will start from default initial value")

    def save_data(self, dae: Dae) -> None:

        for item in self.states:
            self.xf[item] = np.zeros([self.n, dae.nts])
            self.xf[item][:, :] = dae.x_full[self.__dict__[item][:], :]

    def finit(self, dae: Dae) -> None:

        """Initialize the device by setting up setpoints, initial states based on the power flow solution.
            Args:
                dae (Dae): The DAE object used to simulate the system.
        """

        u = SX.sym('', 0)
        u0 = []
        for item in self._setpoints:
            # Set the initial guess for the setpoint
            u0.append(self.__dict__[item])
            # Reset it to be a variable
            self.__dict__[item] = SX.sym(item, self.n)
            # Stack the variable to a single vector
            u = vertcat(u, self.__dict__[item])
        u0 = [item for sublist in u0 for item in sublist]

        # Now subtract the initial network currents from algebraic equations
        for alg in self._algebs:
            dae.g[self.__dict__[alg]] += dae.iinit[self.__dict__[alg]]

        # Algebraic variables are now not symbolic but their init values
        dae.y = dae.yinit.copy()
        self.fgcall(dae)
        # Find the indices of differential equations for this type of generator
        diff = [self.__dict__[arg] for arg in self.states]
        diff_index = [item for sublist in np.transpose(diff) for item in sublist]

        inputs = [vertcat(dae.x[diff_index], u)]
        outputs = [vertcat(dae.f[diff_index], dae.g[self.__dict__['vre']], dae.g[self.__dict__['vim']])]

        power_flow_init = Function('h', inputs, outputs)
        newton_init = rootfinder('G', 'newton', power_flow_init)

        x0 = np.array(list(self._x0.values()) * self.n)
        solution = newton_init(vertcat(x0, u0))
        solution = np.array(solution).flatten()

        # Init only these states
        for s in self.states:
            self.xinit[s] = solution[self.__dict__[s]]

        for idx, s in enumerate(self._setpoints):
            setpoint_range_start = (len(self.states) + idx) * self.n
            self.__dict__[s] = solution[setpoint_range_start:setpoint_range_start + self.n]

        # Now load the initial states into DAE class such that simulation/estimation actually starts from those values
        dae.xinit[diff_index] = solution[:len(self.states) * self.n]

        # Reset the algebraic equations such that they can be used "erneut" from scratch once the "fgcall" is called
        dae.g *= 0
        # Reset the voltages to being again symbolic variables
        dae.y = SX.sym('y', dae.ny)

    def fgcall(self, dae: Dae) -> None:
        """Just a placeholder"""
        pass

    def qcall(self, dae: DaeEst) -> None:
        for item in self.states:
            dae.q_proc_noise_diff_cov_matrix[self.__dict__[item], self.__dict__[item]] = (self._states_noise[item]) ** 2


class Synchronous(DeviceRect):
    """Metaclass for SG in rectangular coordinates"""

    def __init__(self):
        super().__init__()
        self._params.update(
            {'fn': 50, 'H': 30, 'R_s': 0.0, 'x_d': 0.2, 'x_q': 0.2, 'x_dprim': 0.05, 'x_qprim': 0.1, 'T_dprim': 8.0, 'T_qprim': 0.8, 'D': 0.0, 'R': 0.05, 'T1': 0.05, 'T2': 0.5,
             'T3': 1.5, 'KA': 200.0, 'TA': 0.015, 'KF': 1.0, 'TF': 0.1, 'KE': 1.0, 'TE': 0.04, 'Vref': 1.03, 'f': 0.01, 'V_exc': 2.0})
        # Init parameters
        self.fn = np.array([], dtype=float)
        self.H = np.array([], dtype=float)
        self.R_s = np.array([], dtype=float)
        self.x_d = np.array([], dtype=float)
        self.x_q = np.array([], dtype=float)
        self.x_dprim = np.array([], dtype=float)
        self.x_qprim = np.array([], dtype=float)
        self.T_dprim = np.array([], dtype=float)
        self.T_qprim = np.array([], dtype=float)
        self.D = np.array([], dtype=float)
        self.R = np.array([], dtype=float)
        self.T1 = np.array([], dtype=float)
        self.T2 = np.array([], dtype=float)
        self.T3 = np.array([], dtype=float)
        self.KA = np.array([], dtype=float)
        self.TA = np.array([], dtype=float)
        self.KF = np.array([], dtype=float)
        self.TF = np.array([], dtype=float)
        self.KE = np.array([], dtype=float)
        self.TE = np.array([], dtype=float)
        self.Vref = np.array([], dtype=float)
        self.f = np.array([], dtype=float)
        self.V_exc = np.array([], dtype=float)
        self.Sn = np.array([], dtype=float)
        self.Vn = np.array([], dtype=float)
        # Now states
        self.states.extend(['delta', 'omega', 'ed', 'eq', 'pm1', 'pm', 'Ef', 'Ef1', 'Ef2'])
        self.ns = 9
        self.delta = np.array([], dtype=float)
        self.omega = np.array([], dtype=float)
        self.ed = np.array([], dtype=float)
        self.eq = np.array([], dtype=float)
        self.pm1 = np.array([], dtype=float)
        self.pm = np.array([], dtype=float)
        self.Ef = np.array([], dtype=float)
        self.Ef1 = np.array([], dtype=float)
        self.Ef2 = np.array([], dtype=float)
        # Set points
        self._setpoints.update({'Pref': 0.1, 'Vf_ref': 2.0})
        self.Vf_ref = np.array([], dtype=float)
        self.Pref = np.array([], dtype=float)
        self.properties.update({'fplot': True})

    def gcall(self, dae: Dae, i_d: casadi.SX, i_q: casadi.SX):
        # algebraic equations (current balance in rectangular coordinates) + scale the current back to the grid reference power
        dae.g[self.vre] -= self.Sn / dae.Sb * (-i_d * sin(dae.x[self.delta]) + i_q * cos(dae.x[self.delta]))
        dae.g[self.vim] -= self.Sn / dae.Sb * (+i_d * cos(dae.x[self.delta]) + i_q * sin(dae.x[self.delta]))

    def tgov1(self, dae: Dae):
        dae.f[self.pm1] = 1 / self.T1 * (dae.x[self.pm] - dae.x[self.pm1])
        dae.f[self.pm] = 1 / self.T3 * (-dae.x[self.omega] / self.R - dae.x[self.pm] + self.Pref)

    def ieeedc1a(self, dae: Dae):
        dae.f[self.Ef] = 1 / self.TE * (-self.KE * dae.x[self.Ef] + dae.x[self.Ef2])
        dae.f[self.Ef1] = 1 / self.TF * (-dae.x[self.Ef1] + self.KF / self.TE * (dae.x[self.Ef2] - self.KE * dae.x[self.Ef]))
        dae.f[self.Ef2] = 1 / self.TA * (-dae.x[self.Ef2] - self.KA * dae.x[self.Ef1] + self.KA * (self.Vf_ref - sqrt((dae.y[self.vre]) ** 2 + (dae.y[self.vim]) ** 2)))
