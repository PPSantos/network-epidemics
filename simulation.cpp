#include "multi_layer_net.cpp"

int main(int argc, char* argv[]) {

	/**
	  * Simulation flags & parameters.
	  */
	int SEED = 57;

	bool VERBOSE = false;

	// Number of simulations per network.
	int numSim = 250;

	// Total number of steps for each simulation.
	int simulationSteps = 50;

	// Initially infected population size.
	int gamma = 10;

	// Initially aware population size
	// (not counting with infected nodes).
	int phi = 5;

	// Infection rate: [0,1].
	double beta = 0.4;

	// Recovery rate: [0,1].
	double delta = 0.0;

	// Awareness spread rate: [0,1].
	double mu = 0.0;

	// Forgetness rate: [0,1].
	double omega = 0.2;

	// Decay in infection rate for aware nodes: [0,1]
	// For (S,A) node: prob of getting infected = beta*(1-lambda).
	// e.g. lambda = 0.0 -> no effect (no decay).
	// e.g. lambda = 1.0 -> (S,A) don't get infected.
	double lambda = 0.0;

	// Whether to write nodes' states to file.
	bool writeStatesToFile = false;

	// Writing to files time-step.
	int writeToFileStep = 1;

	srand(SEED);
	//srand(time(NULL));

	// Namefiles of the networks to load.
    vector<string> networks;
    networks.push_back("graph_0");
	networks.push_back("graph_1");
	networks.push_back("graph_2");
	networks.push_back("graph_3");
	networks.push_back("graph_4");
	networks.push_back("graph_5");
	networks.push_back("graph_6");
	networks.push_back("graph_7");
	networks.push_back("graph_8");
	networks.push_back("graph_9");

	// Parameter values.
    vector<double> param_values;
    param_values.push_back(0.0);
    param_values.push_back(0.1);
    param_values.push_back(0.2);
    param_values.push_back(0.3);
    param_values.push_back(0.4);
    param_values.push_back(0.5);
    param_values.push_back(0.6);
    param_values.push_back(0.7);
    param_values.push_back(0.8);
    param_values.push_back(0.9);
    param_values.push_back(1.0);

	string net_name;
	int counter;

	for (int i=0; i < param_values.size(); i++) {

		cout << "Mu = " << param_values[i] << endl;

		for (int net=0; net < networks.size(); net++) {

			cout << "Simulating network: " << networks[net] << endl;

			// Create network (second argument is the network name).
			net_name = to_string(param_values[i]).substr(0,3) + "_" + networks[net];
			MultiLayerNetwork MNet(networks[net], net_name);

			MNet.simulateSIS(numSim,
							simulationSteps,
							gamma,
							phi,
							beta,
							delta,
							param_values[i],
							omega,
							lambda,
							VERBOSE,
							writeStatesToFile,
							writeToFileStep);

		}

	}

	/*string net_name;
	int counter;

	for (int i=0; i < param_values.size(); i++) {

		cout << "Mu = " << param_values[i] << endl;

		for (int net_1=0; net_1 < networks.size(); net_1++) {

			for (int net_2=0; net_2 < networks.size(); net_2++) {

				if (net_1 == net_2) {
					continue;
				}

				cout << "Simulating network: " << networks[net_1] << " with " <<  networks[net_2] << endl;

				// Create network (second argument is the network name).
				net_name = to_string(param_values[i]).substr(0,3) + "_" + networks[net_1] + "_" + networks[net_2];
				MultiLayerNetwork MNet(networks[net_1], networks[net_2], net_name);

				MNet.simulateSIS(numSim,
								simulationSteps,
								gamma,
								phi,
								beta,
								delta,
								mu,
								param_values[i],
								lambda,
								VERBOSE,
								writeStatesToFile,
								writeToFileStep);

			}

		}

	}*/

	// Create network (second argument is the network name).
	/*MultiLayerNetwork MNet(networks[0], "Net");

	MNet.simulateSIS(numSim,
					simulationSteps,
					gamma,
					phi,
					beta,
					delta,
					mu,
					omega,
					lambda,
					VERBOSE,
					writeStatesToFile,
					writeToFileStep);*/


	return 0;
	
}