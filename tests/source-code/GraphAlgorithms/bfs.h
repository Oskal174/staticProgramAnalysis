#ifndef _BFS_H_
#define _BFS_H_

#include "main.h"

void BFS(graphNotWeighted &, int);
bool isConnected(graphNotWeighted &, int);
unsigned int connectedComponentsCount(graphNotWeighted &);

#endif // _BFS_H_
