#include<iostream>
#include<sstream>
#include<fstream>
#include<vector>
#include<list>
#include<iterator>
#include<algorithm>
#include <numeric>

using namespace std;

enum State {
	S, // Susceptible.
	I  // Infected.
};

template <typename Iter, typename Cont>
bool isLast(Iter iter, const Cont& cont)
{
	return (iter != cont.end()) && (next(iter) == cont.end());
}

class Network {

	/**
	 *  Undirected network class.
	 */

	private:

		// Number of nodes.
		int N;

		// Adjacency list.
		vector<list<int>>* adj_list;

	public:

		Network(int n_nodes) {
			N = n_nodes;
			adj_list = new vector<list<int>>(N);
		}

		Network(string file_name) {
			/**
			 *	Loads network from file.
			 *
			 *  Arguments:
			 *		- file_name: file name with network description.
			 */
			std::ifstream file(file_name);

			if (file.is_open()) {
				std::string line;

				// Read number of nodes.
				getline(file, line);
				std::istringstream iss(line);
				if (!(iss >> N)) {
					throw runtime_error("Error parsing file.");
				}

				adj_list = new vector<list<int>>(N);

				// Read edges.
				while (getline(file, line)) {

					std::istringstream iss(line);
					int n1, n2;
					if (!(iss >> n1 >> n2)) {
						throw runtime_error("Error parsing file.");
					}

					this->addEdge(n1, n2);
				}
				file.close();
			}

		}

		~Network() {
			delete adj_list;
		}

		void addEdge(int n1, int n2) {
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

			for (int i=0; i < N; i++) {

				cout << "Node " << i << ": [";
				list<int> :: iterator it;

				for (it = adj_list->at(i).begin(); it != adj_list->at(i).end(); it++) {
					if (isLast(it, adj_list->at(i))) {
						cout << *it << "]";	
					} else {
						cout << *it << ",";	
					}
				}
				cout << endl;
			}
		}

		void printNodesState(std::vector<State> states) {
			/**
			 *  Prints nodes state.
			 *  (Used in the simulation context)
			 */
			for (int i=0; i < N; i++) {
				cout << i << ":";
				if (states[i] == State::S) {
					cout << "S ";
				} else if (states[i] == State::I) {
					cout << "I ";
				} else {
					throw "Unknown state";
				}
			}
			cout << endl;
		}

		void simulateSI(int numSim,
						int T,
						double gamma,
						double beta,
						bool verbose,
						bool writeToFile,
						int writeToFileStep) {
			/**
			 *  Simulates SI epidemic spreading process.
			 *
			 *  Arguments:
			 *		- numSim: the number of simulations.
			 *      - T: total number of time steps.
			 *      - gamma: size of initial infected population.
			 *      - beta: infection rate.
			 *      - verbose: whether to print simulation.
			 *      - writeToFile: wheter to write states
			 *                     at each writeToFileStep.
			 *      - writeToFileStep: file writing step.
			 */
			std::list<int> :: iterator it;

			// Store state for each node.
			std::vector<State> states(N);

			// Store nodes that will transit to infected at the next timestep.
			std::vector<int> to_infect;

			for (int sim=0; sim < numSim; sim++) {

				std::fill(states.begin(), states.end(), State::S);

				// Setup initial infected population.
				// Randomly pick gamma individuals to be initially infected.
				std::vector<int> dummy(N);
				std::iota(std::begin(dummy), std::end(dummy), 0);
				std::random_shuffle(dummy.begin(), dummy.end());
				for (int i=0; i < gamma; i++) {
					states[dummy[i]] = State::I;
				}

				for (int t=0; t < T; t++) {

					if (verbose) {
						// Print states.
						cout << "t=" << t << endl;
						this->printNodesState(states);
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

						if (states[node] == State::S) {

							for (it = adj_list->at(node).begin(); it != adj_list->at(node).end(); it++) {

								if (states[*it] == State::I) {

									if (((double) rand() / (RAND_MAX)) < beta) {
										to_infect.push_back(node);
									}
									break;
								}

							}
						}
					}

					// Update states (susceptible -> infected).
					for (int i=0; i < to_infect.size(); i++) {
						states[to_infect[i]] = State::I;
					}
					to_infect.clear();

				}

			}

		}

		void simulateSIS(int numSim,
						int T,
						int gamma,
						double beta,
						double delta,
						bool verbose,
						bool writeToFile,
						int writeToFileStep) {
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
			std::list<int> :: iterator it;

			// Store state for each node.
			std::vector<State> states(N);

			// Store nodes that will transit to
			// infected state at the next timestep.
			std::vector<int> to_infect;

			// Store nodes that will transit to
			// susceptible state at the next timestep.
			std::vector<int> to_recover;

			for (int sim=0; sim < numSim; sim++) {

				std::fill(states.begin(), states.end(), State::S);

				// Setup initial infected population.
				// Randomly pick gamma individuals to be initially infected.
				std::vector<int> dummy(N);
				std::iota(std::begin(dummy), std::end(dummy), 0);
				std::random_shuffle(dummy.begin(), dummy.end());
				for (int i=0; i < gamma; i++) {
					states[dummy[i]] = State::I;
				}

				for (int t=0; t < T; t++) {

					if (verbose) {
						cout << "t=" << t << endl;
						this->printNodesState(states);
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

						if (states[node] == State::S) {

							for (it = adj_list->at(node).begin(); it != adj_list->at(node).end(); it++) {

								if (states[*it] == State::I) {

									if (((double) rand() / (RAND_MAX)) < beta) {
										to_infect.push_back(node);
									}
									break;
								}

							}
						} else if (states[node] == State::I) {

							if (((double) rand() / (RAND_MAX)) < delta) {
								to_recover.push_back(node);
							}
							
						}
					}

					// Update states (susceptible -> infected).
					for (int i=0; i < to_infect.size(); i++) {
						states[to_infect[i]] = State::I;
					}
					to_infect.clear();

					// Update states (infected -> susceptible).
					for (int i=0; i < to_recover.size(); i++) {
						states[to_recover[i]] = State::S;
					}
					to_recover.clear();

				}

			}

			
		}


};


int main(int argc, char* argv[]) {

	// Flags & parameters.
	int SEED = 57;
	bool VERBOSE = true;

	srand(SEED);
	//srand(time(NULL));

	// Namefiles of the networks to load.
    std::vector<string> networks;
    networks.push_back("networks/test_network.txt");

	for (int i=0; i < networks.size(); i++) {

		if (VERBOSE) {
			cout << "Loading network: " << networks[i] << endl;
		}

		// Create network.
		Network Net(networks[i]);
	
		Net.simulateSI(1, 10, 2, 1.0, VERBOSE, true, 1);

		Net.simulateSIS(1, 10, 2, 1.0, 0.0, VERBOSE, true, 1);

	}

	return 0;
}