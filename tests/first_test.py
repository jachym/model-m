import timeit
import click
from seirs_extended import ExtendedNetworkModel, custom_exponential_graph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def demo(numNodes=10000, test_id=None):

    baseGraph = nx.barabasi_albert_graph(n=numNodes, m=9)
    G_normal = custom_exponential_graph(baseGraph, scale=100)

    model = ExtendedNetworkModel(G=G_normal,
                                 beta=0.155,
                                 sigma=1/5.2,
                                 gamma=1/12.39,
                                 mu_I=0.0004,
                                 p=0.2,
                                 beta_D=0.155,
                                 gamma_D=1/12.39,
                                 mu_D=0.0004,
                                 theta_E=0.1,
                                 theta_Ia=0.1,
                                 theta_Is=0.1,
                                 phi_E=0,
                                 phi_Ia=0,
                                 phi_Is=0,
                                 psi_E=1.0,
                                 psi_Ia=1.0,
                                 psi_Is=1.0,
                                 q=0.1,
                                 false_symptoms_rate=0.2,
                                 asymptomatic_rate=0.3,
                                 symptoms_manifest_rate=0.9,
                                 initSSrate=0.2,
                                 initE=0,
                                 initI_n=0.4*numNodes/100,
                                 initI_a=0.2*numNodes/100,
                                 initI_s=0.4*numNodes/100,
                                 initI_d=0,
                                 random_seed=42)

    ndays = 60
    model.run(T=ndays, verbose=True, print_interval=1)
    print("Avg. number of events per day: ", model.tidx/ndays)

    plot = True
    if plot:
        counts = [model.state_counts[s]
                  for s in ("I_n", "I_a", "I_s", "I_d", "E")]
        y = np.sum(counts, axis=0)
        x = model.tseries
        plt.plot(x, y)
        test_id = "_" + test_id if test_id else ""
        plt.savefig(f"num_of_ill{test_id}.png")


@click.command()
@click.argument('n_nodes', default=10000)
@click.argument('test_id', default="")
def test(n_nodes, test_id):
    # demo_fce = lambda: demo(n_nodes)
    # print(timeit.timeit(demo_fce, number=1))
    demo(n_nodes, test_id)


if __name__ == "__main__":
    test()
