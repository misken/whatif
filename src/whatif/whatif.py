import numpy as np
import pandas as pd
from itertools import product
import copy


def create_parameter_grid(scenario_inputs):
    """Create list of dictionaries, each of which corresponds to a set of variable values for a scenario.

    Parameters
    ----------
    scenario_inputs : dict of str to sequence
            Keys are input variable names and values are sequence of values for each scenario for this variable.

    Returns
    -------
    List of dictionaries
    """
    param_grid = []

    keys, values = zip(*scenario_inputs.items())

    for v in product(*values):
        params = dict(zip(keys, v))
        param_grid.append(params)

    return param_grid


def get_sim_results_df(results):
    """Transform raw simulation output dictionary to Pandas ``DataFrame``.

    Parameters
    ----------
    results : list of dictionaries

    Returns
    -------
    Pandas DataFrame
    """
    dfs = []
    for r in results:
        df = pd.DataFrame(r['output'])
        df['scenario_num'] = r['scenario_num']
        for key, val in r['scenario_vals'].items():
            df[key] = val

        dfs.append(df)

    if len(dfs) > 1:
        results_df = pd.concat(dfs)
        return results_df
    else:
        return dfs[0]


class Model():
    """Base class for models"""

    def update(self, param_dict):
        """Update parameter values

        """

        for key in param_dict:
            setattr(self, key, param_dict[key])

    def data_table(self, scenario_inputs, outputs):
        """Create n-inputs by m-outputs data table.

        Parameters
        ----------
        scenario_inputs : dict of str to sequence
            Keys are input variable names and values are sequence of values for each scenario for this variable.

        outputs : list of str
            List of output variable names

        Returns
        -------
        results_df : pandas DataFrame
            Contains values of all outputs for every combination of scenario inputs
        """

        # Clone the model using deepcopy
        model_clone = copy.deepcopy(self)

        # Create parameter grid
        dt_param_grid = list(create_parameter_grid(scenario_inputs))

        # Create the table as a list of dictionaries
        results = []

        # Loop over the scenarios
        for params in dt_param_grid:
            # Update the model clone with scenario specific values
            model_clone.update(params)
            # Create a result dictionary based on a copy of the scenario inputs
            result = copy.copy(params)
            # Loop over the list of requested outputs
            for output in outputs:
                # Compute the output.
                out_val = getattr(model_clone, output)()
                # Add the output to the result dictionary
                result[output] = out_val

            # Append the result dictionary to the results list
            results.append(result)

        # Convert the results list (of dictionaries) to a pandas DataFrame and return it
        results_df = pd.DataFrame(results)
        return results_df

    def goal_seek(self, obj_fn, target, by_changing, a, b, N=100):
        """Approximate solution of f(x)=0 on interval [a,b] by bisection method.

        Parameters
        ----------
        obj_fn : str
            The function name for which we are trying to approximate a solution f(x)=target.
        target : float
            The goal
        by_changing : str
            Name of the input variable in model
        a,b : numbers
            The interval in which to search for a solution. The function returns
            None if (f(a) - target) * (f(b) - target) >= 0 since a solution is not guaranteed.
        N : (positive) integer
            The number of iterations to implement.

        Returns
        -------
        x_N : number
            The midpoint of the Nth interval computed by the bisection method. The
            initial interval [a_0,b_0] is given by [a,b]. If f(m_n) - target == 0 for some
            midpoint m_n = (a_n + b_n)/2, then the function returns this solution.
            If all signs of values f(a_n), f(b_n) and f(m_n) are the same at any
            iteration, the bisection method fails and return None.
        """
        # TODO: Checking of inputs and outputs

        # Clone the model
        model_clone = copy.deepcopy(self)

        # The following bisection search is a direct adaptation of
        # https://www.math.ubc.ca/~pwalls/math-python/roots-optimization/bisection/
        # The changes include needing to use an object method instead of a global function
        # and the inclusion of a non-zero target value.

        setattr(model_clone, by_changing, a)
        f_a_0 = getattr(model_clone, obj_fn)()
        setattr(model_clone, by_changing, b)
        f_b_0 = getattr(model_clone, obj_fn)()

        if (f_a_0 - target) * (f_b_0 - target) >= 0:
            # print("Bisection method fails.")
            return None

        # Initialize the end points
        a_n = a
        b_n = b
        for n in range(1, N + 1):
            # Compute the midpoint
            m_n = (a_n + b_n) / 2

            # Function value at midpoint
            setattr(model_clone, by_changing, m_n)
            f_m_n = getattr(model_clone, obj_fn)()

            # Function value at a_n
            setattr(model_clone, by_changing, a_n)
            f_a_n = getattr(model_clone, obj_fn)()

            # Function value at b_n
            setattr(model_clone, by_changing, b_n)
            f_b_n = getattr(model_clone, obj_fn)()

            # Figure out which half the root is in, or if we hit it exactly, or if the search failed
            if (f_a_n - target) * (f_m_n - target) < 0:
                a_n = a_n
                b_n = m_n
            elif (f_b_n - target) * (f_m_n - target) < 0:
                a_n = m_n
                b_n = b_n
            elif f_m_n == target:
                # print("Found exact solution.")
                return m_n
            else:
                # print("Bisection method fails.")
                return None

        # If we get here we hit iteration limit, return best solution found so far
        return (a_n + b_n) / 2

    def simulate(self, random_inputs, outputs, scenario_inputs=None, keep_random_inputs=False):
        """Simulate model for one or more scenarios

        Parameters
        ----------
        random_inputs : dict of str to sequence of random variates
            Keys are stochastic input variable names and values are sequence of $n$ random variates, where $n$ is the number of simulation replications
        outputs : list of str
            List of output variable names
        scenario_inputs : optional (default is None), dict of str to sequence
            Keys are deterministic input variable names and values are sequence of values for each scenario for this variable. Is consumed by
            scikit-learn ParameterGrid() function. See https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ParameterGrid.html
        keep_random_inputs : optional (default is False), boolean
            If True, all the random input variates are included in the results dataframe

        Returns
        -------
        results : list of dictionaries
            Values of all outputs for each simulation replication. If `scenario_inputs` is not None,
            then there is one dictionary for each combination of scenario inputs, otherwise, there
            is a single dictionary.

            Keys of results list:

            scenario_base_vals -- values of model object attributes
            scenario_num -- int starting at 1
            scenario_vals -- {} if `scenario_inputs` is None, else scenario specific values
            output -- dictionary of `np.array` objects whose keys are the elements of `outputs`
            
        Notes
        -----
        Perhaps add a model assumptions related attribute and associated methods
        """

        # Clone the model
        model_clone = copy.deepcopy(self)

        # Update clone with random_inputs
        model_clone.update(random_inputs)

        # Store raw simulation input values if desired
        if keep_random_inputs:
            scenario_base_vals = vars(model_clone)
        else:
            scenario_base_vals = vars(self)

        # Initialize output counters and containers
        scenario_num = 0
        scenario_results = []

        # Check if multiple scenarios
        if scenario_inputs is not None:
            # Create parameter grid for scenario inputs
            sim_param_grid = list(create_parameter_grid(scenario_inputs))

            # Scenario loop
            for params in sim_param_grid:
                model_clone.update(params)
                # Initialize scenario related outputs
                result = {}
                scenario_vals = copy.copy(params)
                result['scenario_base_vals'] = scenario_base_vals
                result['scenario_num'] = scenario_num
                result['scenario_vals'] = scenario_vals
                raw_output = {}

                # Output measure loop
                for output_name in outputs:
                    output_array = getattr(model_clone, output_name)()
                    raw_output[output_name] = output_array

                # Gather results for this scenario
                result['output'] = raw_output
                scenario_results.append(result)
                scenario_num += 1

            return scenario_results

        else:
            # Similar logic to above, but only a single scenario
            results = []
            result = {}

            result['scenario_base_vals'] = scenario_base_vals
            result['scenario_num'] = scenario_num
            result['scenario_vals'] = {}

            raw_output = {}
            for output_name in outputs:
                output_array = getattr(model_clone, output_name)()
                raw_output[output_name] = output_array

            result['output'] = raw_output
            results.append(result)

            return results
        
    def model_to_df(self, values, columns):
        
        X = np.transpose(np.vstack(values))                
        df = pd.DataFrame(X, columns=columns)

    def __str__(self):
        """
        Print dictionary of object attributes that don't include an underscore as first char
        """
        return str({key: val for (key, val) in vars(self).items() if key[0] != '_'})







