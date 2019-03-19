/****************************************
 * File: main.cpp
 *
 * Author: Kirill Kuzminykh 2016
 ****************************************/

#include <iostream>
#include <fstream>

#include "main.h"
#include "bfs.h"
#include "dfs.h"

using namespace std;

int main() {
	graphNotWeighted G;

	cout << "Graph initialization, enter name of file with graph" << endl;
	string fileName;
	cin >> fileName;

	initGraphFromFile(G, fileName);

	cout << "Done" << endl;

	cout << endl;
	cout << "Available actions:" << endl;
	cout << "Print graph - print" << endl;
	cout << "BFS - bfs" << endl;
	cout << "DFS - dfs" << endl;
	cout << "Strong connected components of Graph - scc" << endl;
	cout << "Topology sort - ts" << endl;
	cout << "Connected check - cc" << endl;
	cout << "Connected components count - cccount" << endl;
	cout << endl;

	while(true) {
		cout << "Action(man for see all, exit for exit): ";
		string action;
		cin >> action;

		if(action == "man") {
			cout << endl;
			cout << "Available actions:" << endl;
			cout << "Print graph - print" << endl;
			cout << "BFS - bfs" << endl;
			cout << "DFS - dfs" << endl;
			cout << "Strong connected components of Graph - scc" << endl;
			cout << "Topology sort - ts" << endl;
			cout << "Connected check - cc" << endl;
			cout << "Connected components count - cccount" << endl;
			cout << endl;
		}
		else if(action == "exit") {
			break;
		}
		else if(action == "print") {
			printGraphNotWeighted(G);
			cout << endl;
		}
		else if(action == "bfs") {
			cout << "Enter start node: ";
			int start;
			cin >> start;

			BFS(G, start);
		}
		else if(action == "dfs") {
			cout << "Recursive?(1/0): ";
			bool recFlag;
			cin >> recFlag;

			DFSInit(G, recFlag);
		}
		else if(action == "scc") {
			vector<graphNotWeighted> components = strongConnectedComponents(G);

			cout << "Components: " << endl;
			for(unsigned int i = 0; i < components.size(); i++) {
				cout << "Component " << i << ':' << endl;
				printGraphNotWeighted(components[i]);
				cout << endl;
			}
		}
		else if(action == "ts") {
			vector<int> result = topologySortInit(G);

			cout << "Result order:" << endl;
			for(unsigned int i = 0; i < result.size(); i++) {
				cout << result[i] << ' ';
			}
			cout << endl;
		}
		else if(action == "cc") {
			cout << "Enter start node: ";
			int start;
			cin >> start;

			bool result = isConnected(G, start);
			if(result) {
				cout << "Graph is conneted" << endl;
			}
			else {
				cout << "Graph is not connected" << endl;
			}
		}
		else if(action == "cccount") {
			unsigned int count = connectedComponentsCount(G);
			cout << "Connected component count: " << count << endl;
		}
		else {
			cout << "wrong action, try again" << endl;
		}
	}

	return 0;
}

void initGraphFromFile(graphNotWeighted &G, string fileName) {
	ifstream file("graphFile");

	unsigned int n = 0;
	unsigned int oriented;
	file >> n >> oriented;

	G.resize(n);

	while (!file.eof()) {
		int a, b;
		file >> a;
		file >> b;

		G[a].push_back(b);
		if(oriented == 0) {
			G[b].push_back(a);
		}
	}

	file.close();

	return;
}

void printGraphNotWeighted(graphNotWeighted &G) {
	for(unsigned int i = 0; i < G.size(); i++) {
			for(unsigned int j = 0; j < G[i].size(); j++) {
				cout << i << ':' << G[i][j] << ' ';
			}
	}
	cout << endl;

	return;
}


