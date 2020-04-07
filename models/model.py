import numpy as np
import scipy as scipy
import scipy.integrate
import networkx as nx

from history_utils import TimeSeries, TransitionHistory


def create_model_base(clsname, states, transitions,
                      final_states=None, invisible_states=None,
                      unstable_states=None,
                      init_arguments={},
                      model_parameters={},
                      calc_propensities="None"):
    """ Creates base model class

    Params:
         states              list of states
         transitions         list of state couples (possible transitions)
         final_states        list of final states (optional)
         invisible_states    states that are not members of population

    Returns:
        class
    """

    # dictionary of future class variables
    attributes = {
        "states": states,
        "transitions": transitions,
        "final_states": final_states,
        "invisible_states": invisible_states,
        "unstable_states": unstable_states or states,
        "fixed_model_parameters": init_arguments,
        "model_parameters": model_parameters,
        "common_arguments": {"random_seed": (None, "random seed value")}
    }

    model_cls = type(clsname, (), attributes)
    doc_text = """    A class to simulate the Stochastic Network Model

    Params:
            G       Network adjacency matrix (numpy array) or Networkx graph object \n"""

    for argname in ("fixed_model_parameters",
                    "model_parameters",
                    "common_arguments"):
        for param, definition in attributes[argname].items():
            param_text = f"            {param}       {definition[1]}\n"
            if argname == "model_parameters":
                param_text += f"            (float or np.array)\n"
            doc_text = doc_text + param_text

    model_cls.__doc__ = doc_text

    # __init__ method
    def init_function(self, G,  **kwargs):

        # 1. set member variables acording to init arguments
        # definition is couple (default value, description)
        self.G = G
        for argdict in (self.fixed_model_parameters,
                        self.common_arguments,
                        self.model_parameters):
            for name, definition in argdict.items():
                value = kwargs.get(name, definition[0])
                setattr(self, name, value)

        # 2. model initialization
        self.inicialization()

        # 3. time and history setup
        self.setup_series_and_time_keeping()

        # 4. init states and their counts
        init_state_counts = {
            s: kwargs.get(f"init_{s}", 0)
            for s in self.states
        }
        print(init_state_counts)
        self.states_and_counts_init(init_state_counts)

        # 5. set callback to None
        self.periodic_update_callback = None

    # add __init__
    model_cls.__init__ = init_function

    # add member functions
    function_list = [inicialization,
                     update_graph,
                     node_degrees,
                     setup_series_and_time_keeping,
                     states_and_counts_init,
                     set_periodic_update,
                     update_scenario_flags,
                     num_contacts,
                     current_state_count,
                     current_N,
                     run_iteration,
                     run,
                     finalize_data_series,
                     increase_data_series_length]

    for function in function_list:
        setattr(model_cls, function.__name__, function)

    def not_implemented_yet(self):
        raise NotImplementedError

    if calc_propensities is None:
        calc_propensities = not_implemented_yet
    else:
        model_cls.calc_propensities = calc_propensities

    return model_cls


def inicialization(self):
    """ model inicialization """

    if self.random_seed:
        np.random.seed(self.random_seed)

    # setup adjacency matrix
    self.update_graph(self.G)

    # create arrays for model params
    for param_name in self.model_parameters:
        param = self.__getattribute__(param_name)
        if isinstance(param, (list, np.ndarray)):
            setattr(self, param_name,
                    np.array(param).reshape((self.num_nodes, 1)))
        else:
            setattr(self, param_name,
                    np.full(fill_value=param, shape=(self.num_nodes, 1)))


def setup_series_and_time_keeping(self):

    self.num_transitions = 100  # TO: change to our situation
    tseries_len = (self.num_transitions + 1) * self.num_nodes

    self.tseries = TimeSeries(tseries_len, dtype=float)

    max_state_len = max([len(s) for s in self.states])
    self.history = TransitionHistory(tseries_len, itemsize=max_state_len)

    # state_counts ... numbers of inidividuals in given states
    self.state_counts = {
        state: TimeSeries(tseries_len, dtype=int)
        for state in self.states
    }

    # N ... actual number of individuals in population
    self.N = TimeSeries(tseries_len, dtype=float)

    # float time
    self.t = 0
    self.tmax = 0  # will be set when run() is called
    self.tidx = 0  # time index to time series
    self.tseries[0] = 0


def states_and_counts_init(self, state_counts):
    """ Initialize Counts of inidividuals with each state """

    for state, init_value in state_counts.items():
        self.state_counts[state][0] = init_value

    nodes_left = self.num_nodes - sum(
        [self.state_counts[s][0] for s in self.states]
    )

    self.state_counts[self.states[0]][0] += nodes_left

    # invisible nodes does not count to population (death ones)
    self.N[0] = self.num_nodes - sum(
        [self.state_counts[s][0] for s in self.invisible_states]
    )

    # X ... array of states
    tempX = []
    for state, count in self.state_counts.items():
        tempX.extend([state]*count[0])
    self.X = np.array(tempX).reshape((self.num_nodes, 1))
    # distribute the states randomly
    np.random.shuffle(self.X)


def update_graph(self, new_G):
    """ create adjacency matrix for G """

    if isinstance(new_G, np.ndarray):
        self.A = scipy.sparse.csr_matrix(new_G)
    elif type(new_G) == nx.classes.graph.Graph:
        # adj_matrix gives scipy.sparse csr_matrix
        self.A = nx.adj_matrix(new_G)
    else:
        raise TypeError(
            "Input an adjacency matrix or networkx object only.")

    self.num_nodes = self.A.shape[1]
    self.degree = np.asarray(self.node_degrees(self.A)).astype(float)

    # if TF_ENABLED:
    #     self.A = to_sparse_tensor(self.A)


def node_degrees(self, Amat):
    """ return number of degrees of  nodes,
    i.e. sums of adj matrix cols """
    # TODO FIX ME
    return Amat.sum(axis=0).reshape(self.num_nodes, 1)


def set_periodic_update(callback):
    """ set callback function 
    callback function is called every midnigh """
    self.periodic_update_callback = callback


# TODO: need this???
def update_scenario_flags(self):
    testing_infected = np.any(self.theta_Ia) or np.any(
        self.theta_Is) or np.any(self.phi_Ia) or np.any(self.phi_Is)
    positive_test_for_I = np.any(self.psi_Ia) or np.any(self.psi_Is)

    testing_exposed = np.any(self.theta_E) or np.any(self.phi_E)
    positive_test_for_E = np.any(self.psi_E)

    self.testing_scenario = (
        (positive_test_for_I and testing_infected) or
        (positive_test_for_E and testing_exposed)
    )

    tracing_E = np.any(self.phi_E)
    tracing_I = np.any(self.phi_Ia) or np.any(self.phi_Is)
    self.tracing_scenario = (
        (positive_test_for_E and tracing_E) or
        (positive_test_for_I and tracing_I)
    )


def num_contacts(self, state):
    """ return numbers of contacts from given state 
    if state is a list, it is sum over all states """

    if type(state) == str:
        # if TF_ENABLED:
        #     with tf.device('/GPU:' + "0"):
        #         x = tf.Variable(self.X == state, dtype="float32")
        #         return tf.sparse.sparse_dense_matmul(self.A, x)
        # else:
        return np.asarray(
            scipy.sparse.csr_matrix.dot(self.A, self.X == state))

    elif type(state) == list:
        state_flags = np.hstack(
            [np.array(self.X == s, dtype=int) for s in state]
        )
        # if TF_ENABLED:
        #     with tf.device('/GPU:' + "0"):
        #         x = tf.Variable(state_flags, dtype="float32")
        #         nums = tf.sparse.sparse_dense_matmul(self.A, x)
        # else:

        nums = scipy.sparse.csr_matrix.dot(self.A, state_flags)
        return np.sum(nums, axis=1).reshape((self.numNodes, 1))
    else:
        raise TypeException(
            "num_contacts(state) accepts str or list of strings")


def current_state_count(self, state):
    return self.state_counts[state][self.tidx]


def current_N(self):
    return self.N[self.tidx]


def increase_data_series_length(self):

    self.tseries.bloat()
    self.history.bloat()
    for state in self.states:
        self.state_counts[state].bloat()
    self.N.bloat()


def finalize_data_series(self):

    self.tseries.finalize(self.tidx)
    self.history.finalize(self.tidx)
    for state in self.states:
        self.state_counts[state].finalize(self.tidx)
    self.N.finalize(self.tidx)


def run_iteration(self):

    if (self.tidx >= self.tseries.len()-1):
        # Room has run out in the timeseries storage arrays; double the size of these arrays
        self.increase_data_series_length()

    # 1. Generate 2 random numbers uniformly distributed in (0,1)
    r1 = np.random.rand()
    r2 = np.random.rand()

    # 2. Calculate propensities
    propensities, transition_types = self.calc_propensities()

    # Terminate when probability of all events is 0:
    if propensities.sum() <= 0.0:
        self.finalize_data_series()
        return False

    # 3. Calculate alpha
    propensities_flat = propensities.ravel(order='F')
    cumsum = propensities_flat.cumsum()
    alpha = propensities_flat.sum()

    # 4. Compute the time until the next event takes place
    tau = (1/alpha)*np.log(float(1/r1))
    self.t += tau

    # 5. Compute which event takes place
    transition_idx = np.searchsorted(cumsum, r2*alpha)
    transition_node = transition_idx % self.num_nodes
    transition_type = transition_types[int(transition_idx/self.num_nodes)]

    # 6. Update node states and data series
    assert(self.X[transition_node] == transition_type[0] and self.X[transition_node] not in self.final_states), "Assertion error: Node " + \
        str(transition_node)+" has unexpected current state " + \
        str(self.X[transition_node]) + \
        " given the intended transition of "+str(transition_type)+"."

    self.X[transition_node] = transition_type[1]

    self.tidx += 1
    self.tseries[self.tidx] = self.t
    self.history[self.tidx] = (transition_node, *transition_type)

    for state in self.states:
        self.state_counts[state][self.tidx] = self.state_counts[state][self.tidx-1]
    self.state_counts[transition_type[0]][self.tidx] -= 1
    self.state_counts[transition_type[1]][self.tidx] += 1

    self.N[self.tidx] = self.N[self.tidx-1]
    # if node died
    if transition_type[1] in (self.invisible_states):
        self.N[self.tidx] = self.N[self.tidx-1] - 1

    # Terminate if tmax reached or num infectious and num exposed is 0:
    numI = sum([self.current_state_count(s)
                for s in self.unstable_states
                ])

    if self.t >= self.tmax or numI < 1:
        self.finalize_data_series()
        return False

    return True


def run(self, T, print_interval=10, verbose=False):

    if not T > 0:
        return False

    self.tmax += T

    running = True
    day = -1

    while running:

        running = self.run_iteration()

        # true after the first event after midnight
        day_changed = day != int(self.t)

        # run periodical update
        if self.periodic_update_callback and day != 1 and day_changed:
            self.periodic_update_callback()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # print only if print_interval is set
        # prints always at the beginning of a new day
        if print_interval or not running:
            if day_changed:
                day = int(self.t)

            if not running or (day_changed and (day % print_interval == 0)):
                print("t = %.2f" % self.t)
                if verbose or not running:
                    for state in self.states:
                        print(f"\t {state} = {self.current_state_count(state)}")
                print(flush=True)

    return True