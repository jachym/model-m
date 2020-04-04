import timeit
import click
from seirs_extended import ExtendedNetworkModel, custom_exponential_graph
import networkx as nx
import matplotlib.pyplot as plt


def demo(numNodes=10000):

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


@click.command()
@click.argument('n_nodes', default=10000)
def test(n_nodes):
    # demo_fce = lambda: demo(n_nodes)
    # print(timeit.timeit(demo_fce, number=1))
    demo(n_nodes)


if __name__ == "__main__":
    test()
