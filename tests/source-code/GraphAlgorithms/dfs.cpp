#include <iostream>
#include <stack>
#include <algorithm>

#include "main.h"
#include "dfs.h"

using namespace std;

int currentTime;

void DFSInit(graphNotWeighted &G, bool recursive) {
	int n = G.size();

	vector<int> distance(n, -1);
	vector<int> prevTop(n, -1);
	vector<int> time(n, -1);
	vector<char> topColor(n, 'w');

	currentTime = 0;

	for(int v = 0; v < n; v++) {
		if(topColor[v] == 'w') {
			if(recursive == true) {
				DFSRecursive(G, v, distance, prevTop, time, topColor);
			}
			else {
				DFSInStack(G, v, distance, prevTop, time, topColor);
			}
		}
	}

	//Print results
	for (int i = 0; i < prevTop.size(); i++) {
		cout << i << '(' << distance[i] << ',' << time[i] << ")  :";
		int x = prevTop[i];
		while (x != -1) {
			cout << x << ' ';
			x = prevTop[x];
		}
		cout << endl;
	}
	cout << endl;

	return;
}

void DFSRecursive(
		graphNotWeighted &G,
		int start,
		vector<int> &distance,
		vector<int> &prevTop,
		vector<int> &time,
		vector<char> &topColor) {

	currentTime++;
	distance[start] = currentTime;
	topColor[start] = 'g';
	for (int i = 0; i < G[start].size(); i++) {
		int u = G[start][i];

		if (topColor[u] == 'w') {
			prevTop[u] = start;
			DFSRecursive(G, u, distance, prevTop, time, topColor);
		}
	}

	topColor[start] = 'b';
	currentTime++;
	time[start] = currentTime;

	return;
}

void DFSInStack(
		graphNotWeighted &G,
		int start,
		vector<int> &distance,
		vector<int> &prevTop,
		vector<int> &time,
		vector<char> &topColor) {

	stack<pair<int, int> > S;

	S.push(make_pair(start, -1));
	topColor[start] = 'g';
	currentTime++;
	distance[start] = currentTime;
	while (S.size()) {
		int v = S.top().first;
		int u = S.top().second;

		int w = -1;
		for (int i = 0; i < G[v].size(); i++)
			if (G[v][i] != u && topColor[G[v][i]] == 'w') {
				w = G[v][i];
				break;
			}

		if (w == -1) {
			S.pop();
			topColor[v] = 'b';
			currentTime++;
			time[v] = currentTime;
		}
		else {
			S.top().second = w;
			if (topColor[w] == 'w') {
				prevTop[w] = v;
				S.push(make_pair(w, -1));
				currentTime++;
				distance[w] = currentTime;
				topColor[w] = 'g';
			}
		}
	}

	return;
}

vector<int> topologySortInit(graphNotWeighted &G) {
	int n = G.size();
	vector<int> resultOrder;
	vector<char> color(n, 'w');

	for (int v = 0; v < n; v++)
		if (color[v] == 'w')
			topologySortProc(G, v, color, resultOrder);

	reverse(resultOrder.begin(), resultOrder.end());

	return resultOrder;
}

void topologySortProc(graphNotWeighted &G, int start, vector<char> &color, vector<int> &order) {
	stack<pair<int, int> > S;

	S.push(make_pair(start, -1));
	color[start] = 'g';
	while (S.size()) {
		int v = S.top().first;
		int u = S.top().second;

		int w = -1;
		for (int i = 0; i < G[v].size(); i++)
			if (G[v][i] != u && color[G[v][i]] == 'w') {
				w = G[v][i];
				break;
			}

		if (w == -1) {
			S.pop();
			color[v] = 'b';
			order.push_back(v);
		}
		else {
			S.top().second = w;
			if (color[w] == 'w') {
				S.push(make_pair(w, -1));
				color[w] = 'g';
			}
		}
	}

	return;
}

graphNotWeighted transposingGraph(graphNotWeighted &G) {
	int n = G.size();
	graphNotWeighted GT(n);

	vector<int> count(n);
	for (int i = 0; i < n; i++)
		for (int j = 0; j < G[i].size(); j++)
			count[G[i][j]]++;

	for (int i = 0; i < n; i++)
		GT[i].reserve(count[i]);

	for (int i = 0; i < n; i++)
		for (int j = 0; j < G[i].size(); j++)
			GT[G[i][j]].push_back(i);

	return GT;
}

graphNotWeighted getComponent(graphNotWeighted &G, int start, vector<char> &color) {
	stack<pair<int, int> > S;
	graphNotWeighted component(G.size());

	bool isEmpty = false;
	for(int p = 0; p < G[start].size(); p++)
		if(color[G[start][p]] == 'w')
			isEmpty = true;

	if(isEmpty == false) {
		component[start].push_back(start);
		color[start] = 'b';
		return component;
	}

	S.push(make_pair(start, -1));
	while (S.size()) {
		int v = S.top().first;
		int u = S.top().second;

		int w = -1;
		for (int i = 0; i < G[v].size(); i++)
			if (G[v][i] != u && color[G[v][i]] == 'w') {
				w = G[v][i];
				break;
			}

		if (w == -1) {
			S.pop();
			color[v] = 'b';
		}
		else {
			S.top().second = w;
			if (color[w] == 'w') {
				component[w].push_back(v);
				S.push(make_pair(w, -1));
				color[w] = 'g';
			}
		}
	}

	return component;
}

vector<graphNotWeighted> strongConnectedComponents(graphNotWeighted &G) {
	int n = G.size();

	vector<int> order = topologySortInit(G);

	graphNotWeighted GT = transposingGraph(G);

	vector<graphNotWeighted> strongConnectedComponents;
	vector<char> color(n, 'w');
	for (int i = 0; i < n; i++)
		if (color[order[i]] == 'w')
			strongConnectedComponents.push_back(getComponent(GT, order[i], color));

	return strongConnectedComponents;
}




