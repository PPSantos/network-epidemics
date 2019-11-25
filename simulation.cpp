#include<iostream>
#include<sstream>
#include<fstream>
#include<vector>
#include<list>
#include<iterator>
#include<algorithm>
#include<numeric>

using namespace std;

enum Disease_State {
	S, // Susceptible.
	I  // Infected.
};

enum Awareness_State {
	A, // Aware.
	U  // Unaware.
};

template <typename Iter, typename Cont>
bool isLast(Iter iter, const Cont& cont)
{
	return (iter != cont.end()) && (next(iter) == cont.end());
}

class MultiLayerNetwork {

	/**
	 *  Undirected two layer network class.
	 */

	private:

		// Number of nodes.
		int N;

		// Adjacency lists.
		vector<list<int>>* disease_net;
		vector<list<int>>* awareness_net;

		// Network's name.
		string network_name;

	public:

		MultiLayerNetwork(int n_nodes) {
			N = n_nodes;
			disease_net = new vector<list<int>>(N);
			awareness_net = new vector<list<int>>(N);
			network_name = "Default";
		}

		MultiLayerNetwork(string file_name, string net_name) {
			/**
			 *	Loads network from file.
			 *	(Both networks will have the same topology)
			 *	
			 *
			 *  Arguments:
			 *		- file_name: network file name.
			 *		- net_name: network name.
			 */
			ifstream file("networks/" + file_name + ".txt");

			if (file.is_open()) {
				string line;

				// Read number of nodes.
				getline(file, line);
				istringstream iss(line);
				if (!(iss >> N)) {
					throw runtime_error("Error parsing file.");
				}

				disease_net = new vector<list<int>>(N);
				awareness_net = new vector<list<int>>(N);

				// Read edges.
				while (getline(file, line)) {

					istringstream iss(line);
					int n1, n2;
					if (!(iss >> n1 >> n2)) {
						throw runtime_error("Error parsing file.");
					}

					this->addEdge(n1, n2, disease_net);
					this->addEdge(n1, n2, awareness_net);
				}
				file.close();
			}

			network_name = net_name;

		}

		MultiLayerNetwork(string file_name_1, string file_name_2, string net_name) {
			/**
			 *	Loads network from file.
			 *	(Different networks' topology)
			 *	
			 *
			 *  Arguments:
			 *		- file_name_1: file name with disease network description.
			 *		- file_name_2: file name with awareness network description.
			 *		- net_name: network name.
			 */
			ifstream file("networks/" + file_name_1 + ".txt");

			if (file.is_open()) {
				string line;

				// Read number of nodes.
				getline(file, line);
				istringstream iss(line);
				if (!(iss >> N)) {
					throw runtime_error("Error parsing file.");
				}

				disease_net = new vector<list<int>>(N);

				// Read edges.
				while (getline(file, line)) {

					istringstream iss(line);
					int n1, n2;
					if (!(iss >> n1 >> n2)) {
						throw runtime_error("Error parsing file 1.");
					}

					this->addEdge(n1, n2, disease_net);
				}
				file.close();
			}

			ifstream file_2("networks/" + file_name_2 + ".txt");

			if (file_2.is_open()) {
				string line;

				// Read number of nodes.
				getline(file_2, line);
				istringstream iss(line);
				if (!(iss >> N)) {
					throw runtime_error("Error parsing file 2.");
				}

				awareness_net = new vector<list<int>>(N);

				// Read edges.
				while (getline(file_2, line)) {

					istringstream iss(line);
					int n1, n2;
					if (!(iss >> n1 >> n2)) {
						throw runtime_error("Error parsing file 2.");
					}

					this->addEdge(n1, n2, awareness_net);
				}
				file_2.close();
			}

			network_name = net_name;

		}

		~MultiLayerNetwork() {
			delete disease_net;
			delete awareness_net;
		}

		void addEdge(int n1, int n2, vector<list<int>>* adj_list) {
			adj_list->at(n1).push_back(n2);
			adj_list->at(n2).push_back(n1);
		}

		void printNetworkInfo() {
			/**
			 *  Prints network info.
			 *  (Number of nodes and adjacency list)
			 */
			cout << "Network info:" << endl;
			cout << "N=" << N << endl;

			cout << "Disease spreading network:" << endl;
			for (int i=0; i < N; i++) {

				cout << "Node " << i << ": [";
				list<int> :: iterator it;

				for (it = disease_net->at(i).begin(); it != disease_net->at(i).end(); it++) {
					if (isLast(it, disease_net->at(i))) {
						cout << *it << "]";	
					} else {
						cout << *it << ",";	
					}
				}
				cout << endl;
			}

			cout << "Awareness spreading network:" << endl;
			for (int i=0; i < N; i++) {

				cout << "Node " << i << ": [";
				list<int> :: iterator it;

				for (it = awareness_net->at(i).begin(); it != awareness_net->at(i).end(); it++) {
					if (isLast(it, awareness_net->at(i))) {
						cout << *it << "]";	
					} else {
						cout << *it << ",";	
					}
				}
				cout << endl;
			}

		}

		void printNodesStates(vector<Disease_State> disease_states,
							  vector<Awareness_State> awareness_states) {
			/**
			 *  Prints nodes state.
			 *  (Used in the simulation context)
			 */
			for (int i=0; i < N; i++) {
				cout << i << ":";
				if (disease_states[i] == Disease_State::S) {
					cout << "(S,";
				} else if (disease_states[i] == Disease_State::I) {
					cout << "(I,";
				} else {
					throw "Unknown disease state";
				}

				if (awareness_states[i] == Awareness_State::U) {
					cout << "U) ";
				} else if (awareness_states[i] == Awareness_State::A) {
					cout << "A) ";
				} else {
					throw "Unknown awareness state";
				}
			}
			cout << endl;
		}

		void simulateSI(int numSim,
						int T,
						int gamma,
						int phi,
						double beta,
						double mu,
						double lambda,
						bool verbose,
						bool writeStatesToFile,
						int writeToFileStep) {
			/**
			 *  Simulates SI epidemic spreading process
			 *	(two layer network scenario).
			 *
			 *  Arguments:
			 *		- numSim: the number of simulations.
			 *
			 *      - T: total number of time steps.
			 *
			 *      - gamma: size of initial infected population.
			 *
			 *      - phi: size of initial aware population,
			 *				excluding the initially infected nodes
			 *				(because infected are always aware).
			 *
			 *      - beta: infection rate.
			 *
			 *		- mu: awareness spread rate.
			 *
		     *		- lambda: Value between 0 and 1 (percentage)
			 *					representing how much beta will decrease
			 *					if the node is in the (S,A) state.
			 *				  	I.e., for (S,A) node:
			 *					probability of getting infected = beta*(1-lambda).
			 *
			 *      - verbose: whether to print simulation.
			 *
			 *      - writeStatesToFile: wheter to write states
			 *                     at each writeStatesToFileStep.
			 *
			 *      - writeToFileStep: file writing step.
			 */
			int counter;
			list<int> :: iterator it;

			// Store the disease state for each node.
			vector<Disease_State> disease_states(N);

			// Store the awareness state for each node.
			vector<Awareness_State> awareness_states(N);

			// Store nodes that will transit to infected at the next timestep.
			vector<int> to_infect;

			// Store nodes that will transit to aware at the next timestep.
			vector<int> to_aware;

			// Infected average ratio per time-step.
			vector<double> infected_ratios(T, 0.0);

			for (int sim=0; sim < numSim; sim++) {

				// Reset all nodes to (S,U).
				fill(disease_states.begin(), disease_states.end(), Disease_State::S);
				fill(awareness_states.begin(), awareness_states.end(), Awareness_State::U);

				// Setup initial infected population.
				// Randomly pick gamma individuals to be initially infected.
				// Note that infected nodes are always aware.
				// Initialize (I,A) nodes.
				vector<int> dummy(N);
				iota(begin(dummy), end(dummy), 0);
				random_shuffle(dummy.begin(), dummy.end());
				for (int i=0; i < gamma; i++) {
					disease_states[dummy[i]] = Disease_State::I;
					awareness_states[dummy[i]] = Awareness_State::A;
				}

				// Setup initially aware but not infected nodes.
				// Initialize (S,A) nodes.
				for (int i=gamma; i < (gamma + phi); i++) {
					awareness_states[dummy[i]] = Awareness_State::A;
				}

				for (int t=0; t < T; t++) {

					if (verbose) {
						// Print states.
						cout << "t=" << t << endl;
						this->printNodesStates(disease_states, awareness_states);
					}

					if (writeStatesToFile && (t % writeToFileStep == 0)) {

						// Write disease states to file.
						ofstream file;
						file.open ("output/" + network_name + "_disease_states.csv", ios_base::app);
						for (int i=0; i < (N-1); i++) {
							file << disease_states[i] << ",";
						}
						file << disease_states[N-1];
						file << "\n";
						file.close();

						// Write awareness states to file.
						file.open ("output/" + network_name + "_awareness_states.csv", ios_base::app);
						for (int i=0; i < (N-1); i++) {
							file << awareness_states[i] << ",";
						}
						file << awareness_states[N-1];
						file << "\n";
						file.close();
					}

					counter = 0;
					for (int node=0; node < N; node++) {
						if (disease_states[node] == Disease_State::I) {
							counter++;
						}
					}
					infected_ratios[t] += ((float) counter / (float) N) / (float) numSim;

					for (int node=0; node < N; node++) {

						// Disease network transitions.
						if (disease_states[node] == Disease_State::S) {

							for (it = disease_net->at(node).begin(); it != disease_net->at(node).end(); it++) {

								if (disease_states[*it] == Disease_State::I) {

									if (awareness_states[node] == Awareness_State::U) {
										// (S,U) - Susceptible and unaware.

										if (((double) rand() / (RAND_MAX)) < beta) {
											to_infect.push_back(node);
											to_aware.push_back(node);
										}
										break;

									} else {
										// (S,A) - Susceptible and aware.

										if (((double) rand() / (RAND_MAX)) < (beta*(1-lambda))) {
											to_infect.push_back(node);
											to_aware.push_back(node);
										}
										break;

									}

								}

							}

						}

						// Awareness network transitions.
						if (awareness_states[node] == Awareness_State::U) {
							// (S,U) - Susceptible and unaware.

								for (it = awareness_net->at(node).begin(); it != awareness_net->at(node).end(); it++) {

									if (awareness_states[*it] == Awareness_State::A) {

										if (((double) rand() / (RAND_MAX)) < mu) {
											to_aware.push_back(node);
										}
										break;
									}

								}

						}

					}

					// Update states (susceptible -> infected).
					for (int i=0; i < to_infect.size(); i++) {
						disease_states[to_infect[i]] = Disease_State::I;
					}
					to_infect.clear();

					// Update states (unaware -> aware).
					for (int i=0; i < to_aware.size(); i++) {
						awareness_states[to_aware[i]] = Awareness_State::A;
					}
					to_aware.clear();

				}

			}

			// Write infected ratios to file.
			ofstream file;
			file.open ("output/" + network_name + "_infected_ratios.csv");
			for (int i=0; i < (T-1); i++) {
				file << infected_ratios[i] << ",";
			}
			file << infected_ratios[T-1];
			file << "\n";
			file.close();

		}

		void simulateSIS(int numSim,
						int T,
						int gamma,
						double beta,
						double delta,
						bool verbose,
						bool writeToFile,
						int writeToFileStep) {

			throw "Not implemented";
			/**
			 *  Simulates SIS epidemic spreading process.
			 *
			 *  Arguments:
			 *		- numSim: the number of simulations.
			 *      - T: total number of time steps.
			 *      - gamma: size of initial infected population.
			 *      - beta: infection rate.
			 *      - delta: recovery rate. 
			 *      - verbose: whether to print simulation.
			 *      - writeToFile: wheter to write states
			 *                     at each writeToFileStep.
			 *      - writeToFileStep: file writing step.
			 *
			 */
			/*
			std::list<int> :: iterator it;

			// Store state for each node.
			std::vector<Disease_State> states(N);




			// TODO.
			std::vector<Awareness_State> awareness_states(N);



			// Store nodes that will transit to
			// infected state at the next timestep.
			std::vector<int> to_infect;

			// Store nodes that will transit to
			// susceptible state at the next timestep.
			std::vector<int> to_recover;

			for (int sim=0; sim < numSim; sim++) {

				std::fill(states.begin(), states.end(), Disease_State::S);

				// Setup initial infected population.
				// Randomly pick gamma individuals to be initially infected.
				std::vector<int> dummy(N);
				std::iota(std::begin(dummy), std::end(dummy), 0);
				std::random_shuffle(dummy.begin(), dummy.end());
				for (int i=0; i < gamma; i++) {
					states[dummy[i]] = Disease_State::I;
				}

				for (int t=0; t < T; t++) {

					if (verbose) {
						cout << "t=" << t << endl;
						this->printNodesStates(states, awareness_states);
					}

					if (writeToFile && (t % writeToFileStep == 0)) {
						// Write states to file.
						std::ofstream file;
						file.open ("output/states.csv", std::ios_base::app);
						for (int i=0; i < (N-1); i++) {
							file << states[i] << ",";
						}
						file << states[N-1];
						file << "\n";
						file.close();
					}

					for (int node=0; node < N; node++) {

						if (states[node] == Disease_State::S) {

							for (it = disease_net->at(node).begin(); it != disease_net->at(node).end(); it++) {

								if (states[*it] == Disease_State::I) {

									if (((double) rand() / (RAND_MAX)) < beta) {
										to_infect.push_back(node);
									}
									break;
								}

							}
						} else if (states[node] == Disease_State::I) {

							if (((double) rand() / (RAND_MAX)) < delta) {
								to_recover.push_back(node);
							}
							
						}
					}

					// Update states (susceptible -> infected).
					for (int i=0; i < to_infect.size(); i++) {
						states[to_infect[i]] = Disease_State::I;
					}
					to_infect.clear();

					// Update states (infected -> susceptible).
					for (int i=0; i < to_recover.size(); i++) {
						states[to_recover[i]] = Disease_State::S;
					}
					to_recover.clear();

				}

			}*/

		}

};


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