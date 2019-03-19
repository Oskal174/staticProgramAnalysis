#ifndef _MAIN_H_
#define _MAIN_H_

#include <vector>
#include <string>

using std::string;
using std::vector;

typedef vector< vector<int> > graphNotWeighted;

void initGraphFromFile(graphNotWeighted &, string);
void printGraphNotWeighted(graphNotWeighted &);

#endif // _MAIN_H_
