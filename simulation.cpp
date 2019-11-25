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
	int phi = 0;

	// Infection rate: [0,1].
	//double beta = 0.8;

	// Awareness spread rate: [0,1].
	double mu = 0.0;

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

	/**
	 *	Simulate beta.
	 */
	string net_name;

	for (int i=0; i < param_values.size(); i++) {

		cout << "Beta = " << param_values[i] << endl;

		for (int j=0; j < networks.size(); j++) {

			cout << "Simulating network: " << networks[j] << endl;

			// Create network (second argument is the network name).
			net_name = to_string(param_values[i]).substr(0,3) + "_" + networks[j];
			MultiLayerNetwork MNet(networks[j], net_name);

			MNet.simulateSI(numSim,
							simulationSteps,
							gamma,
							phi,
							param_values[i],
							mu,
							lambda,
							VERBOSE,
							writeStatesToFile,
							writeToFileStep);

		}

	}

	return 0;
}