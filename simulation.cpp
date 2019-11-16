#include<iostream>
#include<list>
#include<vector>
#include<iterator>
#include <fstream>

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
     *  Base class: Undirected Network.
     */

    protected:

        // Number of nodes.
        int N;

        // Adjacency list.
        vector<list<int>>* adj_list;

    public:

        Network(int n_nodes) {
            N = n_nodes;
            adj_list = new vector<list<int>>(N);
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

        void printNodesState(vector<State>* states) {
            /**
             *  Prints nodes state.
             *  (Used in the simulation context)
             */
            for (int i=0; i < N; i++) {
                cout << i << ":";
                if (states->at(i) == State::S) {
                    cout << "S ";
                } else if (states->at(i) == State::I) {
                    cout << "I ";
                } else {
                    throw "Unknown state";
                }
            }
            cout << endl;
        }

        void simulateSI(int T,
                        vector<int> &inits,
                        double beta,
                        bool verbose,
                        bool writeToFile,
                        int writeToFileStep) {
            /**
             *  Simulates SI epidemic spreading process.
             *
             *  Arguments:
             *      - T: total number of time steps.
             *      - inits: initial infected population
             *              (list of initially infected nodes).
             *      - beta: infection rate.
             *      - verbose: whether to print simulation.
             *      - writeToFile: wheter to write states
             *                     at each writeToFileStep.
             *      - writeToFileStep: file writing step.
             */
            list<int> :: iterator it;

            // Store state for each node.
            vector<State>* states = new vector<State>(N, State::S);

            // Store nodes that will transit to infected at the next timestep.
            vector<int> to_infect;

            // Setup initial infected population.
            for (int i=0; i < inits.size(); i++) {
                states->at(inits[i]) = State::I;
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
                        file << states->at(i) << ",";
                    }
                    file << states->at(N-1);
                    file << "\n";
                    file.close();
                }

                for (int node=0; node < N; node++) {

                    if (states->at(node) == State::S) {

                        for (it = adj_list->at(node).begin(); it != adj_list->at(node).end(); it++) {

                            if (states->at(*it) == State::I) {

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
                    states->at(to_infect[i]) = State::I;
                }
                to_infect.clear();

            }

            delete states;
        }

        void simulateSIS(int T,
                        vector<int> &inits,
                        double beta,
                        double delta,
                        bool verbose,
                        bool writeToFile,
                        int writeToFileStep) {
            /**
             *  Simulates SI epidemic spreading process.
             *
             *  Arguments:
             *      - T: total number of time steps.
             *      - inits: initial infected population
             *              (list of initially infected nodes).
             *      - beta: infection rate.
             *      - delta: recovery rate. 
             *      - verbose: whether to print simulation.
             *      - writeToFile: wheter to write states
             *                     at each writeToFileStep.
             *      - writeToFileStep: file writing step.
             *
             */
            list<int> :: iterator it;

            // Store state for each node.
            vector<State>* states = new vector<State>(N, State::S);

            // Store nodes that will transit to
            // infected stateat the next timestep.
            vector<int> to_infect;

            // Store nodes that will transit to
            // susceptible state at the next timestep.
            vector<int> to_recover;

            // Setup initial infected population.
            for (int i=0; i < inits.size(); i++) {
                states->at(inits[i]) = State::I;
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
                        file << states->at(i) << ",";
                    }
                    file << states->at(N-1);
                    file << "\n";
                    file.close();
                }

                for (int node=0; node < N; node++) {

                    if (states->at(node) == State::S) {

                        for (it = adj_list->at(node).begin(); it != adj_list->at(node).end(); it++) {

                            if (states->at(*it) == State::I) {

                                if (((double) rand() / (RAND_MAX)) < beta) {
                                    to_infect.push_back(node);
                                }
                                break;
                            }

                        }
                    } else if (states->at(node) == State::I) {

                        if (((double) rand() / (RAND_MAX)) < beta) {  
                            to_recover.push_back(node);
                        }
                        
                    }
                }

                // Update states (susceptible -> infected).
                for (int i=0; i < to_infect.size(); i++) {
                    states->at(to_infect[i]) = State::I;
                }
                to_infect.clear();

                // Update states (infected -> susceptible).
                for (int i=0; i < to_recover.size(); i++) {
                    states->at(to_recover[i]) = State::S;
                }
                to_recover.clear();

            }

            delete states;
        }


};


class SmallNetwork : public Network {
    public:
        SmallNetwork() : Network(9) {

            this->addEdge(0, 4);
            this->addEdge(5, 4);
            this->addEdge(6, 4);
            this->addEdge(1, 4);
            this->addEdge(1, 2);
            this->addEdge(4, 3);
            this->addEdge(3, 7);
            this->addEdge(8, 7);
            this->addEdge(8, 3);
            
        }
};


class RandomNetwork : public Network {
    public:
        RandomNetwork(int n_nodes, double p) : Network(n_nodes) {

            // Randomly initialize adjacency list.
            for (int i=0; i < N; i++) {
                for (int j=0; j < N; j++) {
                    if (i != j) {
                        if (((double) rand() / (RAND_MAX)) < p) {
                            this->addEdge(i,j);
                        }
                    }
                }
            }
            
        }
};


int main(int argc, char* argv[]) {

    //int SEED = 57;
    //srand(SEED);
    srand(time(NULL));

    SmallNetwork SNet;
    SNet.printNetworkInfo();

    vector<int> inits {2,8};

    //SNet.simulateSI(10, inits, 1.0, true, true, 1);

    SNet.simulateSIS(200, inits, 0.1, 0.9, true, true, 1);

    return 0;
}