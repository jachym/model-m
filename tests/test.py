import numpy as np
from model import create_custom_model
from romeo_juliet_graph_gen import RomeoAndJuliet as Verona
from run_experiment import magic_formula

model_definition = {
    "states": ["S", "I", "R", "D"],
    "transitions":  [("S", "I"), ("I", "R"), ("R", "S"), ("I", "D")],
    "final_states": ["D"],
    "invisible_states": ["D"],
    "init_arguments": {},
    "model_parameters": {"beta": (0.5, "pst of transition to anather state"),
                         "gamma": (0.02, "death rate")}
}

# note: I use "self" since it will become a method of a model class
# self is object model


def calc_propensities(self):
    """ example of propensities function 
    you will typically use information from graph here 
    use self.A, self.num_contacts, etc.  
    """
    propensities = {}
    for t in self.transitions:
        propensities[t] = self.beta * \
            (self.X == t[0]) * self.num_contacts("I") / self.current_N()
    propensities[("I", "D")] = self.gamma * (self.X == "I")

    propensities_list = []
    for t in self.transitions:
        propensities_list.append(propensities[t])
    stacked_propensities = np.hstack(propensities_list)

    return stacked_propensities, self.transitions


def calc_propensities(model): return raise NotImplementedError


SIRDModel = create_custom_model("SIRDModel", **model_definition,
                                calc_propensities=calc_propensities)


g = Verona()
A = magic_formula(g.as_dict_of_graphs(), g.get_layers_info())


model = SIRDModel(A, beta=0.5, gamma=0.2, init_I=5)
print(model.__doc__)

print(model.states)
model.run(60, verbose=True, print_interval=5)
