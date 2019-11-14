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

        void printNodeInfo(int n) {
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
                if (isLast(it,adj_list->at(n))) {
                    cout << *it << "])";	
                } else {
                    cout << *it << ",";	
                }
    
            }
            cout << endl;

        }

        void prinfInfo() {
            cout << "Graph info:" << endl;
            for (int i = 0; i < N; i++) {
                printNodeInfo(i);
            }
        }

};

int main(int argc, char* argv[]) {

    int N = 6;

    Graph G(N);

    printf("Number of nodes: %d\n", G.getN());

    G.prinfInfo();

    G.addEdge(0, 4);
    G.addEdge(0, 3);
    G.addEdge(1, 2);
    G.addEdge(1, 4);
    G.addEdge(1, 5);
    G.addEdge(2, 3);
    G.addEdge(2, 5);
    G.addEdge(5, 3);
    G.addEdge(5, 4);

    G.prinfInfo();

    return 0;
    
}