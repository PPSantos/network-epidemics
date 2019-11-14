#include<iostream>
#include<list>
#include<vector>
#include<iterator>

using namespace std;

enum State {
    S, // Susceptible.
    I  // Infected.
};


class Graph {
    /**
     *  Undirected graph.
     */

    // Number of nodes.
    int N;

    // Adjacency list.
    vector<list<int>>* adj_list;

    // States vector.
    vector<State>* states;

    public:

        Graph(int n_nodes) {
            N = n_nodes;

            // Initialize adjacency list.
            adj_list = new vector<list<int>>(N);
            
            // Initialize states vector.
            states = new vector<State>(N, State::S);
        }

        ~Graph() {
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

        void printStates() {
            cout << "States: ";
            for (int i = 0; i < (N-1); i++) {
                if (states->at(i) == State::S) {
                    cout << i << "-" << "S" << ",";
                } else if (states->at(i) == State::I) {
                    cout << i << "-" << "I" << ",";
                }
            }
            if (states->at(N-1) == State::S) {
                    cout << N-1 << "-" << "S" << endl;
            } else if (states->at(N-1) == State::I) {
                    cout << N-1 << "-" << "I" << endl;
            }
        }

        void printAdjList() {
            cout << "Adjacency list: ";

        }
};


int main(int argc, char* argv[]) {

    int N = 6;

    Graph G(N);

    printf("Number of nodes: %d\n", G.getN());

    G.addEdge(0, 4);
    G.addEdge(0, 3);
    G.addEdge(1, 2);
    G.addEdge(1, 4);
    G.addEdge(1, 5);
    G.addEdge(2, 3);
    G.addEdge(2, 5);
    G.addEdge(5, 3);
    G.addEdge(5, 4);

    G.printStates();

    return 0;
    
}