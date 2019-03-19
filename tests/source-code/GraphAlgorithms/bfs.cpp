#include <ostream>
#include <iostream>
#include <queue>

#include "main.h"

using std::cout;
using std::endl;
using std::queue;

void BFS(graphNotWeighted &G, int start) {
	queue<int> Q;
	vector<int> distance(G.size(), -1);
	vector<int> prevTop(G.size(), -1);

	distance[start] = 0;
	Q.push(start);
	while (Q.size()) {
		int u = Q.front();
		Q.pop();
		for (int j = 0; j < G[u].size(); j++) {
			int v = G[u][j];
			if (distance[v] == -1) {
				distance[v] = distance[u] + 1;
				prevTop[v] = u;
				Q.push(v);
			}
		}
	}

	//print results
	for (int i = 0; i < prevTop.size(); i++) {
		cout << i << '(' << distance[i] << ")\t:";
		int x = prevTop[i];
		while (x != -1) {
			cout << x << ' ';
			x = prevTop[x];
		}
		cout << endl;
	}

	return;
}

bool isConnected(graphNotWeighted &G, int start) {
	queue<int> Q;
	vector<int> distance(G.size(), -1);
	vector<int> prevTop(G.size(), -1);

	distance[start] = 0;
	Q.push(start);
	while (Q.size()) {
		int u = Q.front();
		Q.pop();
		for (int j = 0; j < G[u].size(); j++) {
			int v = G[u][j];
			if (distance[v] == -1) {
				distance[v] = distance[u] + 1;
				prevTop[v] = u;
				Q.push(v);
			}
		}
	}

	//print results
	for (int i = 0; i < G.size(); ++i)
			if (distance[i] == -1)
				return false;

	return true;
}

unsigned int connectedComponentsCount(graphNotWeighted &G) {
	queue<int> Q;
	vector<int> distance(G.size(), -1);
	vector<int> prevTop(G.size(), -1);

	unsigned int count = 0;
	for(int start = 0; start < G.size(); start++) {
		if(distance[start] == -1) {
			distance[start] = 0;
			Q.push(start);
			while (Q.size()) {
				int u = Q.front();
				Q.pop();
				for (int j = 0; j < G[u].size(); j++) {
					int v = G[u][j];
					if (distance[v] == -1) {
						distance[v] = distance[u] + 1;
						prevTop[v] = u;
						Q.push(v);
					}
				}
			}

		count++;
		}
	}

	return count;
}


