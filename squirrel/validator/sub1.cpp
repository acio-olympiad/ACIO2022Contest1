#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <cassert>

using namespace std;

// Note: Not actually a good validator
int N, maxdegree, cnt;
vector<int> g[100005];

int dfs(int x, int p) {
  cnt++;
  int res = 0;
  for (int c : g[x]) if (c != p) {
    res = max(res, dfs(c, x) + 1);
  }
  return res;
}

int main() {
  scanf("%d", &N);
  assert(1 <= N);
  assert(N <= 100000);
  for (int i = 0; i < N-1; i++) {
    int a, b;
    scanf("%d %d", &a, &b);
    g[a].push_back(b);
    g[b].push_back(a);
  }
  for (int i = 1; i <= N; i++) maxdegree = max(maxdegree, (int)g[i].size());
  int furthest = dfs(1, 1);
  assert(cnt == N);

  assert(N <= 1000);
  return 0;
}
