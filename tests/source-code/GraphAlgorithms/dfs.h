#ifndef _DFS_H_
#define _DFS_H_

#include "main.h"

void DFSInit(graphNotWeighted &, bool);
void DFSRecursive(graphNotWeighted &, int start, vector<int> &, vector<int> &, vector<int> &, vector<char> &);
void DFSInStack(graphNotWeighted &, int start, vector<int> &, vector<int> &, vector<int> &, vector<char> &);

vector<int> topologySortInit(graphNotWeighted &);
void topologySortProc(graphNotWeighted &, int, vector<char> &, vector<int> &);

graphNotWeighted transposingGraph(graphNotWeighted &);
graphNotWeighted getComponent(graphNotWeighted &, int, vector<char> &);
vector<graphNotWeighted> strongConnectedComponents(graphNotWeighted &);

#endif // _DFS_H_
