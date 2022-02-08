#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>

using namespace std;

int N;
vector<int> g[100005];

int dfs(int x, int p) {
  int res = 0;
  for (int c : g[x]) if (c != p) {
    res = max(res, dfs(c, x) + 1);
  }
  return res;
}

int main() {
  scanf("%d", &N);
  for (int i = 0; i < N-1; i++) {
    int a, b;
    scanf("%d %d", &a, &b);
    g[a].push_back(b);
    g[b].push_back(a);
  }
  int furthest = dfs(1, 1);
  printf("%d\n", (N-1)*2 - furthest + 1);
  return 0;
}
