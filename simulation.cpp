#include<iostream>
#include<list>
#include<vector>
#include<iterator>

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
     *  Undirected Network.
     */

    protected:
        // Number of nodes.
        int N;

        // Adjacency list.
        vector<list<int>>* adj_list;

        // States vector.
        vector<State>* states;

    public:

        Network(int n_nodes) {
            N = n_nodes;

            // Initialize adjacency list.
            adj_list = new vector<list<int>>(N);
            
            // Initialize states vector.
            states = new vector<State>(N, State::S);
        }

        ~Network() {
            delete adj_list;
            delete states;
        }

        int getN() {
            return N;
        }

        void addEdge(int n1, int n2) {
            adj_list->at(n1).push_back(n2);
            adj_list->at(n2).push_back(n1);
        }

        void printNodeInfo(int n) {
            /**
             *  Prints node info.
             *  (Infection state and neighbours)
             */
            cout << "Node " << n << ": (";
            if (states->at(n) == State::S) {
                cout << "S, [";
            } else if (states->at(n) == State::I) {
                cout << "I, [";
            } else {
                throw "Unknown state";
            }

            list<int> :: iterator it;
            for (it = adj_list->at(n).begin(); it != adj_list->at(n).end(); it++) {
                if (isLast(it, adj_list->at(n))) {
                    cout << *it << "])";	
                } else {
                    cout << *it << ",";	
                }
    
            }
            cout << endl;

        }

        void printInfo() {
            /**
             *  Prints network info.
             */
            cout << "Network info:" << endl;
            for (int i = 0; i < N; i++) {
                printNodeInfo(i);
            }
        }

        void simulateSI(int T, vector<int> &inits, double beta) {
            /**
             *  Simulates SI epidemic spreading process.
             *
             *  Arguments:
             *      - T: total number of time steps.
             *      - inits: initial infected population
             *              (list of intially infected nodes).
             *      - beta: infection rate.
             *
             */
            list<int> :: iterator it;

            // Keep track of the infection times for each node.
            vector<int> infection_time(N,-1);

            // Initial infected population.
            for (int i = 0; i < inits.size(); i++) {
                states->at(inits[i]) = State::I;
            }

            for (int t = 0; t < T; t++) {

                cout << "t=" << t << endl;
                this->printInfo();

                for (int node = 0; node < N; node++) {
                    
                    if (states->at(node) == State::S) {

                        for (it = adj_list->at(node).begin(); it != adj_list->at(node).end(); it++) {

                            if ((states->at(*it) == State::I) &&
                                (infection_time[*it] != t) &&
                                (((double) rand() / (RAND_MAX)) < beta)) {

                                states->at(node) = State::I;
                                infection_time[node] = t;

                            }

                        }

                    }
                }
            }
        }

};

class RandomNetwork : public Network {

    public:
        RandomNetwork(int n_nodes, double p) : Network(n_nodes) {

            // Randomly initialize adjacency list.
            for (int i = 0; i < Network::N; i++) {
                for (int j = 0; j < this->N; j++) {
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

    int SEED = 57;
    srand(SEED);

    int N = 9;

    Network G(N);

    printf("Number of nodes: %d\n", G.getN());

    G.addEdge(0, 4);
    G.addEdge(5, 4);
    G.addEdge(6, 4);
    G.addEdge(1, 4);
    G.addEdge(1, 2);
    G.addEdge(4, 3);
    G.addEdge(3, 7);
    G.addEdge(8, 7);
    G.addEdge(8, 3);

    //G.printInfo();

    //RandomNetwork R(N, 0.5);

    //R.prinfInfo();

    vector<int> inits;
    inits.push_back(2);
    G.simulateSI(10, inits, 0.5);
    G.simulateSI(10, inits, 0.5);

    return 0;

}