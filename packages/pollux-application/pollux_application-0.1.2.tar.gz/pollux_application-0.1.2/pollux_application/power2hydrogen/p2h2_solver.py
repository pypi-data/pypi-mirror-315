from pollux_application.application_abstract import ApplicationAbstract
from pollux_model.power_supply.power_supply_profiles import PowerSupply
from pollux_model.power_demand.power_demand_profiles import PowerDemand
from pollux_model.hydrogen_demand.hydrogen_demand_profiles import HydrogenDemand
from pollux_model.splitter.splitter import Splitter
from pollux_model.adder.adder import Adder
from pollux_model.electrolyser.electrolyser_physics_based import ElectrolyserDeGroot
from pollux_model.gas_storage.hydrogen_tank_model import HydrogenTankModel
from pollux_model.solver.solver import Solver
from pollux_model.solver.step_function import StepFunction
from pollux_model.solver.key_performance_indicators import Objective, rmse

import json
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
import os


def convert_ndarray_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert ndarray to list
    elif isinstance(obj, dict):
        return {
            key: convert_ndarray_to_list(value) for key, value in obj.items()
        }  # Recurse for dicts
    elif isinstance(obj, list):
        return [convert_ndarray_to_list(item) for item in obj]  # Recurse for lists
    else:
        return obj  # Return the object if it is not ndarray, dict, or list


class Power2Hydrogen(ApplicationAbstract):
    def __init__(self):
        super().__init__()
        # Scenario
        self.scenario = dict()

        # Parameters
        self.time_horizon = None
        self.step_size_control = None
        self.time_vector = []
        self.time_vector_control = []
        self.splitter1_control = []

        # Input profiles
        self.power_supply_profile = []
        self.power_demand_profile = []
        self.hydrogen_demand_profile = []

        # Controls
        self.splitter1_control = dict()
        self.splitter2_control = dict()
        self.hydrogen_storage_control = dict()
        self.components_with_control = []
        self.control_init = None
        self.control_scaled_value = []
        self.control_reshaped = []

        # Components
        self.power_supply = None
        self.power_demand = None
        self.splitter1 = None
        self.electrolyser = None
        self.splitter2 = None
        self.adder = None
        self.hydrogen_storage = None
        self.hydrogen_demand = None

        # Solver
        self.solver = None

        # Optimisation
        self.function_value = []

        # Outputs
        self.outputs = dict()
        self.kpis = dict()

    def init_parameters(self, input):
        """Function to initialize the model parameters"""
        # TODO: Make it flexible so it can load multiple components

        ##########################################################################
        # Setting up time arrays for user input profiles and for the control
        ##########################################################################
        if isinstance(input["time_horizon"], str):
            self.time_horizon = int(input["time_horizon"])
        else:
            self.time_horizon = input["time_horizon"]

        # Assign control timestep value
        if isinstance(input["time_step"], str):
            self.step_size_control = int(input["time_step"])
        else:
            self.step_size_control = input["time_step"]

        if self.time_horizon % self.step_size_control != 0:
            raise ValueError(
                f"time_horizon ({self.time_horizon}) is not divisible \
                              by step_size_control ({self.step_size_control})"
            )

        self.time_vector = np.linspace(0, self.time_horizon, self.time_horizon + 1)[:-1]
        time_vector_control = np.linspace(
            0, self.time_horizon, self.time_horizon // self.step_size_control + 1
        )
        zeros_array = np.zeros(len(time_vector_control))

        mode = input["mode"]

        # Load profiles
        if mode == "simulation":
            required_profiles = [
                "power_demand",
                "hydrogen_demand",
                "power_supply",
                "splitter1",
                "splitter2",
                "hydrogen_storage",
            ]
        elif mode == "optimisation":
            required_profiles = ["power_demand", "hydrogen_demand", "power_supply"]

        missing_profiles = [
            profile
            for profile in required_profiles
            if profile not in input["control_parameters"]
        ]

        if missing_profiles:
            print(
                f"Error: The following profiles are missing: {', '.join(missing_profiles)}"
            )
        else:
            profiles = input["control_parameters"]
            if mode == "simulation":
                self.power_demand_profile = profiles["power_demand"]["data"]
                self.hydrogen_demand_profile = profiles["hydrogen_demand"]["data"]
                self.power_supply_profile = profiles["power_supply"]["data"]

                self.splitter1_control = profiles["splitter1"]["data"]
                self.splitter2_control = profiles["splitter2"]["data"]
                self.hydrogen_storage_control = profiles["hydrogen_storage"]["data"]

            elif mode == "optimisation":
                self.power_demand_profile = profiles["power_demand"]["data"]
                self.hydrogen_demand_profile = profiles["hydrogen_demand"]["data"]
                self.power_supply_profile = profiles["power_supply"]["data"]

        # Check if the division of the time_horizon over the step_size_control is an integer
        if self.time_horizon % self.step_size_control != 0:
            raise ValueError(
                f"time_horizon ({self.time_horizon}) is not divisible by step_size_control ({self.step_size_control})"
            )
        self.time_vector = np.linspace(0, self.time_horizon, 97)
        # self.time_vector_control = np.linspace(0, 24, 25)  # From t=0 to t=24 with 25 steps
        self.time_vector_control = np.linspace(
            0, self.time_horizon, self.time_horizon // self.step_size_control + 1
        )

        ##########################################################################
        # Defining time profiles for supply and demand
        ##########################################################################
        # POWER SUPPLY
        self.power_supply = PowerSupply()
        self.power_supply.set_time_function(self.power_supply_func)

        # POWER DEMAND
        self.power_demand = PowerDemand()
        self.power_demand.set_time_function(self.power_demand_func)

        # HYDROGEN DEMAND
        self.hydrogen_demand = HydrogenDemand()
        self.hydrogen_demand.set_time_function(self.hydrogen_demand_func)

        ##########################################################################
        # Setting up the components
        ##########################################################################
        # SPLITTER 1 (Power splitter)
        step_function = StepFunction(zeros_array, self.step_size_control)
        self.splitter1 = Splitter()
        self.splitter1.set_time_function(step_function)

        # SPLITTER 2 (Hydrogen splitter)
        step_function = StepFunction(zeros_array, self.step_size_control)
        self.splitter2 = Splitter()
        self.splitter2.set_time_function(step_function)

        # ELECTROLYSER
        self.electrolyser = ElectrolyserDeGroot()

        electrolyser_param = input["component_parameters"]["electrolyser_parameters"]
        param = dict()
        param["T_cell"] = float(electrolyser_param["T_cell"])  # cell temperature in K
        param["p_cathode"] = (
            float(electrolyser_param["P_cathode"]) * 10e5
        )  # cathode pressure in Pa
        param["p_anode"] = (
            float(electrolyser_param["P_anode"]) * 10e5
        )  # anode pressure in Pa
        param["p_0_H2O"] = float(electrolyser_param["P_0_H2O"]) * 10e5  # Pa
        param["eta_Faraday_array"] = float(
            electrolyser_param["eta_Faraday"]
        )  # just a constant, in reality is a variable
        param["Faraday_const"] = float(
            electrolyser_param["Faraday_const"]
        )  # Faraday constant [(s A)/mol]
        param["delta_t"] = np.diff(self.time_vector)[0] * 3600  # timestep in seconds
        param["A_cell"] = float(electrolyser_param["A_cell"])  # area in m2
        param["cell_type"] = electrolyser_param["cell_type"]
        param["capacity"] = (
            float(electrolyser_param["capacity"]) * 10e6
        )  # capacity in Watt
        self.electrolyser.update_parameters(param)

        # HYDROGE STORAGE
        step_function = StepFunction(zeros_array, self.step_size_control)
        self.hydrogen_storage = HydrogenTankModel()
        self.hydrogen_storage.set_time_function(step_function)

        hydrogen_storage_param = input["component_parameters"][
            "hydrogen_storage_parameters"
        ]
        param = dict()
        param["timestep"] = (
            np.diff(self.time_vector)[0] * 3600
        )  # should be taken equal to delta_t
        param["maximum_capacity"] = float(
            hydrogen_storage_param["storage_capacity"]
        )  # kg
        param["initial_mass"] = float(hydrogen_storage_param["initial_mass"])  # kg
        self.hydrogen_storage.update_parameters(param)

        # ADDER
        # TODO: Retrieve input from GUI
        self.adder = Adder()
        u = dict()
        u["input_0"] = 0
        u["input_1"] = 0
        self.adder.input = u

        # A list to retrieve object by their names.
        components = {
            "power_supply": self.power_supply,
            "power_demand": self.power_demand,
            "splitter1": self.splitter1,
            "electrolyser": self.electrolyser,
            "splitter2": self.splitter2,
            "adder": self.adder,
            "hydrogen_storage": self.hydrogen_storage,
            "hydrogen_demand": self.hydrogen_demand,
        }

        if mode == "simulation":
            self.components_with_control = [
                "splitter1",
                "splitter2",
                "hydrogen_storage",
            ]

            # Initial value guess. This is the super control vector containing all control variables
            control_init_list = []
            for component in self.components_with_control:
                component_control = f"{component}_control"
                component_control_dict = getattr(self, component_control)

                # create a list from the profile dictionary
                component_control_value = [
                    component_control_dict[str(i)]
                    for i in sorted(component_control_dict.keys(), key=int)
                ]
                control_init_list = control_init_list + component_control_value

            self.control_init = np.array(control_init_list)

        elif mode == "optimisation":
            # List of components with control. For now: number of controls per component are equal
            # TODO: retrieve the components with control from the diagram
            self.components_with_control = [
                "splitter1",
                "splitter2",
                "hydrogen_storage",
            ]

            # Initial value guess. This is the super control vector containing all control variables
            control_array_len = int(self.time_horizon / self.step_size_control)
            init_value_list = []
            for component in self.components_with_control:
                control_param = input["control_parameters"][component]
                initial_value = control_param["initial_value"]
                current_list = [initial_value] * control_array_len
                init_value_list = init_value_list + current_list
            self.control_init = np.array(init_value_list)

        # The controls of the components are updated with values provided by the json input file
        number_of_components_with_control = len(self.components_with_control)
        self.control_reshaped = self.control_init.reshape(
            number_of_components_with_control, -1
        )
        for ii in range(number_of_components_with_control):
            components[self.components_with_control[ii]].update_time_function(
                self.control_reshaped[ii]
            )

        # Solver object
        self.solver = Solver(self.time_vector, components, self.components_with_control)

        # Connect components
        self.connect_components()

    def power_supply_func(self, t):
        profile = self.power_supply_profile
        units_scaling = 1e6  # In MW

        if not (0 <= t <= 24):
            raise ValueError("Time `t` must be in the range [0, 24].")
        times = sorted(float(k) for k in profile.keys())
        for i in range(len(times) - 1):
            if times[i] <= t < times[i + 1]:
                return units_scaling * profile[str(int(times[i]))]

        return (
            units_scaling * profile["23"]
        )  # If t=24, return the value at '23' (the last key)

    # power demand
    def power_demand_func(self, t):
        profile = self.power_demand_profile
        units_scaling = 1e6  # In MW

        if not (0 <= t <= 24):
            raise ValueError("Time `t` must be in the range [0, 24].")
        times = sorted(float(k) for k in profile.keys())
        for i in range(len(times) - 1):
            if times[i] <= t < times[i + 1]:
                return units_scaling * profile[str(int(times[i]))]

        return (
            units_scaling * profile["23"]
        )  # If t=24, return the value at '23' (the last key)

    # hydrogen demand
    def hydrogen_demand_func(self, t):
        profile = self.hydrogen_demand_profile
        units_scaling = 1 / 3600  # In kg/s, profile should be in kg/hour

        if not (0 <= t <= 24):
            raise ValueError("Time `t` must be in the range [0, 24].")
        times = sorted(float(k) for k in profile.keys())
        for i in range(len(times) - 1):
            if times[i] <= t < times[i + 1]:
                return units_scaling * profile[str(int(times[i]))]

        return (
            units_scaling * profile["23"]
        )  # If t=24, return the value at '23' (the last key)

    def connect_components(self):
        """Function to connect components"""

        # Connect the components.
        # Ordering is important here. For now we assume a fixed configuration.
        # The ordering can be calculated to generalise the implementation but is not done yet.
        self.solver.connect(self.power_supply, self.splitter1, "power_supply", "input")
        self.solver.connect(
            self.splitter1, self.power_demand, "output_0", "power_input"
        )
        self.solver.connect(
            self.splitter1, self.electrolyser, "output_1", "power_input"
        )
        self.solver.connect(self.electrolyser, self.splitter2, "massflow_H2", "input")
        self.solver.connect(self.splitter2, self.adder, "output_0", "input_0")
        self.solver.connect(
            self.splitter2, self.hydrogen_storage, "output_1", "mass_flow_in"
        )
        self.solver.connect(
            self.hydrogen_storage, self.adder, "mass_flow_out", "input_1"
        )
        self.solver.connect(
            self.adder, self.hydrogen_demand, "output", "hydrogen_input"
        )

    def calculate(self, input):
        """Function to run the solver"""
        mode = input["mode"]
        optimisation_method = input["optimisation_method"]
        if mode == "optimisation" and optimisation_method == "trust-constr":
            objective_name = "kpi_rmse_demand"
        elif mode == "simulation":
            objective_name = ""
        if objective_name == "":
            ##########################################################################
            # Run the solver, loop over time
            ##########################################################################
            # self.control_init = None
            self.solver.run(self.control_init)  # run the solver with the initial values
        else:
            ##########################################################################
            # Run an optimisation
            ##########################################################################
            # Bounds
            # Retrieve upper and lower bound values from input
            control_array_len = int(self.time_horizon / self.step_size_control)
            lb_value_list = np.array([])
            ub_value_list = np.array([])
            for component in self.components_with_control:
                control_param = input["control_parameters"][component]
                lb_value = control_param["lower_bound"]
                current_lb_list = np.array([lb_value] * control_array_len)
                lb_value_list = np.concatenate((lb_value_list, current_lb_list))

                ub_value = control_param["upper_bound"]
                current_ub_list = np.array([ub_value] * control_array_len)
                ub_value_list = np.concatenate((ub_value_list, current_ub_list))

            # Scale of bounds for maintain equal effect of bounds for each component
            scaling_factor = np.array(ub_value_list)
            bounds = [
                (
                    lb_value_list[ii] / scaling_factor[ii],
                    ub_value_list[ii] / scaling_factor[ii],
                )
                for ii in range(len(self.control_init))
            ]

            control_init_scaled = [
                (self.control_init[ii] / scaling_factor[ii])
                for ii in range(len(self.control_init))
            ]

            # objective function
            objective = Objective(self.solver, scaling_factor)
            objective_function = getattr(objective, objective_name)
            # Note: objective function is function of scaled control

            # method='trust-constr', 'SLSQP', 'L-BFGS-B', 'Nelder-Mead'
            method = input["optimisation_method"]

            match method:
                case "trust-constr":

                    def call_back(x, convergence):
                        self.function_value.append(objective_function(x))
                        self.control_scaled_value.append(x)

                    result = minimize(
                        objective_function,
                        control_init_scaled,
                        method=method,
                        tol=1e-6,
                        options={
                            "maxiter": input["maxiter"],
                            "verbose": True,
                            "disp": True,
                            "finite_diff_rel_step": input["finite_diff_step"],
                        },
                        bounds=bounds,
                        callback=call_back,
                    )

                case "L-BFGS-B":

                    def call_back(x):
                        self.function_value.append(objective_function(x))
                        self.control_scaled_value.append(x)

                    result = minimize(
                        objective_function,
                        control_init_scaled,
                        method=method,
                        options={
                            "maxiter": input["optimisation"]["maxiter"],
                            "verbose": True,
                            "disp": True,
                            # absolute stepsize:
                            "eps": input["optimisation"]["finite_diff_step"],
                            "ftol": 1e-16,
                        },
                        bounds=bounds,
                        callback=call_back,
                    )
                case "Powell":
                    # TNC does only do one iteration, not clear why. dont use it for now!
                    # Powell has a reporting issue result.x does not reproduce reported
                    # minimal objective function value. below an attempt to repair it in
                    # the callback function. Powell seems however very efficient.
                    def call_back(x):
                        self.function_value.append(objective_function(x))
                        iteration = len(self.function_value)
                        if iteration >= 3:
                            minimum = min(self.function_value[:-2])
                            if self.function_value[-1] > minimum:
                                self.control_scaled_value.append(
                                    self.control_scaled_value[-1]
                                )
                            else:
                                self.control_scaled_value.append(x)
                        else:
                            self.control_scaled_value.append(x)

                    result = minimize(
                        objective_function,
                        control_init_scaled,
                        method=method,
                        options={
                            "maxiter": input["optimisation"]["maxiter"],
                            "verbose": True,
                            "disp": True,
                            # absolute stepsize
                            "eps": input["optimisation"]["finite_diff_step"],
                            "return_all": True,
                            # 'maxfun': 10000,
                            # 'stpmax': 0.001
                        },
                        bounds=bounds,
                        callback=call_back,
                    )

                case "differential-evolution":

                    def call_back(x, convergence=None):
                        self.function_value.append(objective_function(x))
                        self.control_scaled_value.append(x)

                    result = differential_evolution(
                        objective_function,
                        maxiter=input["optimisation"]["maxiter"],
                        bounds=bounds,
                        callback=call_back,
                    )

            self.function_value = np.array(self.function_value)
            self.control_scaled_value = np.array(self.control_scaled_value)
            print(f"Objective function values: {self.function_value}")
            control_scaled = result.x  # optimized control
            control = np.array(
                [
                    control_scaled[ii] * scaling_factor[ii]
                    for ii in range(len(control_scaled))
                ]
            )

            number_of_components_with_control = len(self.components_with_control)
            self.control_reshaped = control.reshape(
                number_of_components_with_control, -1
            )
            for ii in range(number_of_components_with_control):
                print(f"control variables {self.components_with_control[ii]}")
                print(f"Optimized solution: {self.control_reshaped[ii]}")
            print(f"Objective function value: {result.fun}")

            # Do a run with optimized control
            self.solver.run(control)

    def get_output(self):
        output_dict = dict()

        output_dict["power_supply_outputs"] = self.solver.outputs[self.power_supply]
        output_dict["splitter1_outputs"] = self.solver.outputs[self.splitter1]
        output_dict["power_demand_outputs"] = self.solver.outputs[self.power_demand]
        output_dict["hydrogen_demand_outputs"] = self.solver.outputs[
            self.hydrogen_demand
        ]
        output_dict["electrolyser_outputs"] = self.solver.outputs[self.electrolyser]
        output_dict["splitter2_outputs"] = self.solver.outputs[self.splitter2]
        output_dict["hydrogen_storage_outputs"] = self.solver.outputs[
            self.hydrogen_storage
        ]
        output_dict["adder_outputs"] = self.solver.outputs[self.adder]

        # Power profiles [MW]
        output_dict["power_supply"] = [
            row[0] * 1e-6 for row in output_dict["power_supply_outputs"]
        ]
        output_dict["power_delivered"] = [
            row[0] * 1e-6 for row in output_dict["splitter1_outputs"]
        ]  # output_0
        output_dict["electrolyser_power_input"] = [
            row[1] * 1e-6 for row in output_dict["splitter1_outputs"]
        ]  # output_1
        output_dict["power_demand"] = [
            row[0] * 1e-6 for row in output_dict["power_demand_outputs"]
        ]
        output_dict["power_difference"] = [
            (output_dict["power_demand"][ii] - output_dict["power_delivered"][ii])
            / output_dict["power_demand"][ii]
            for ii in range(len(output_dict["power_demand"]))
        ]

        # Hydrogen profiles
        output_dict["hydrogen_electrolyser_mass_flow_out"] = [
            row[3] * 3600 for row in output_dict["electrolyser_outputs"]
        ]  # massflow_H2
        output_dict["hydrogen_electrolyser_to_demand"] = [
            row[0] * 3600 for row in output_dict["splitter2_outputs"]
        ]  # output_0
        output_dict["hydrogen_electrolyser_to_storage"] = [
            row[1] * 3600 for row in output_dict["splitter2_outputs"]
        ]  # output_1
        output_dict["hydrogen_demand"] = [
            row[0] * 3600 for row in output_dict["hydrogen_demand_outputs"]
        ]
        output_dict["hydrogen_delivered"] = [
            row[0] * 3600 for row in output_dict["adder_outputs"]
        ]
        output_dict["hydrogen_difference"] = [
            (output_dict["hydrogen_demand"][ii] - output_dict["hydrogen_delivered"][ii])
            / output_dict["hydrogen_demand"][ii]
            for ii in range(len(output_dict["hydrogen_demand"]))
        ]

        # Hydrogen storage profiles
        output_dict["hydrogen_mass_stored"] = [
            row[0] for row in output_dict["hydrogen_storage_outputs"]
        ]
        output_dict["fill_level"] = [
            row[1] * 100 for row in output_dict["hydrogen_storage_outputs"]
        ]
        output_dict["hydrogen_storage_mass_flow_out"] = [
            row[2] * 3600 for row in output_dict["hydrogen_storage_outputs"]
        ]
        output_dict["hydrogen_storage_mass_flow_in"] = [
            row[1] * 3600 for row in output_dict["splitter2_outputs"]
        ]  # output_1

        # KPI profiles
        # conversion factor kg (H2)/hr to MW=MJ/s
        output_dict["conversion_factor_hydrogen"] = 0.0333
        output_dict["efficiency_electrolyser"] = [
            100
            * output_dict["conversion_factor_hydrogen"]
            * output_dict["hydrogen_electrolyser_mass_flow_out"][ii]
            / output_dict["electrolyser_power_input"][ii]
            for ii in range(len(output_dict["electrolyser_power_input"]))
        ]

        ##########################################################################
        # Calculate KPIs
        ##########################################################################
        kpis_dict = dict()
        # KPIs
        kpis_dict["kpi_rmse_power_demand"] = rmse(
            output_dict["power_demand"], output_dict["power_delivered"]
        )  # MW
        kpis_dict["kpi_rmse_hydrogen_demand"] = rmse(
            output_dict["hydrogen_demand"], output_dict["hydrogen_delivered"]
        )  # [kg/hr]
        kpis_dict["kpi_rmse_hydrogen_demand"] = (
            0.03333 * kpis_dict["kpi_rmse_hydrogen_demand"]
        )
        kpis_dict["kpi_rmse_demand"] = (
            kpis_dict["kpi_rmse_power_demand"] + kpis_dict["kpi_rmse_hydrogen_demand"]
        )

        print(
            f"KPI, rmse of power demand and power delivered {kpis_dict['kpi_rmse_power_demand']} [MW]"
        )
        print(
            f"KPI, rmse of hydrogen demand and hydrogen delivered {kpis_dict['kpi_rmse_hydrogen_demand']} [MW]"
        )
        print(f"KPI, sum of rmse of demand {kpis_dict['kpi_rmse_demand']} [MW]")

        electrolyser_power_input_sum = sum(output_dict["electrolyser_power_input"])
        hydrogen_electrolyser_mass_flow_out_sum = 0.03333 * sum(
            output_dict["hydrogen_electrolyser_mass_flow_out"]
        )
        efficiency_electrolyser_total = (
            100 * hydrogen_electrolyser_mass_flow_out_sum / electrolyser_power_input_sum
        )
        print(f"KPI, Efficiency electrolyser {efficiency_electrolyser_total} [-]")

        self.outputs = output_dict
        self.kpis = kpis_dict

    def save_results(
        self, project_folder, project_name, scenario_name, mode, solver_param
    ):
        output_dir = os.path.join(project_folder, project_name, "results")
        os.makedirs(output_dir, exist_ok=True)

        # Create output filenames
        output_filename = os.path.join(
            output_dir, f"{project_name}_{scenario_name}_{mode}_output.json"
        )

        outputs_dict = convert_ndarray_to_list(self.outputs)
        kpis_dict = convert_ndarray_to_list(self.kpis)
        solver_param_dict = convert_ndarray_to_list(solver_param)

        results_dict = {
            "outputs": outputs_dict,
            "kpis": kpis_dict,
            "solver_param": solver_param_dict,
        }

        with open(output_filename, "w") as output_file:
            json.dump(results_dict, output_file, indent=4)
