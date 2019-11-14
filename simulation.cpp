#include<iostream>
#include<list>
#include<iterator>
#include<vector>

using namespace std;

void displayAdjList(list<int> adj_list[], int v) {
  for(int i = 0; i<v; i++) {
     cout << i << "--->";
     list<int> :: iterator it;
     for(it = adj_list[i].begin(); it != adj_list[i].end(); ++it) {
        cout << *it << " ";
     }
     cout << endl;
   }
}

void add_edge(list<int> adj_list[], int u, int v) {   //add v into the list u, and u into list v
   adj_list[u].push_back(v);
   adj_list[v].push_back(u);
}

enum State {
    SUSCEPTIBLE,
    INFECTED
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
            states = new vector<State>(N);
        }

        int getN() {
            return N;
        }

        void addEdge(int n1, int n2) {
            adj_list->at(n1).push_back(n2);
            adj_list->at(n2).push_back(n1);
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

    //displayAdjList(adj_list, v);
    
    return 0;
}