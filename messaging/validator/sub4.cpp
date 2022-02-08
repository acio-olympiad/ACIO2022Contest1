#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <cassert>
using namespace std;

int N, M, ans;
vector<int> g[100005];
int grp[100005], num[100005], seen[100005];

int tot;

void dfs(int x, int setto) {
  grp[x-1] = setto;
  seen[x] = 1;
  for (int v : g[x]) {
    if (!seen[v]) dfs(v, setto);
  }
}

int main() {
  scanf("%d %d", &N, &M);
  assert(1 <= N && N <= 1000);
  assert(0 <= M && M <= 100000);
  for (int i = 0; i < M; i++) {
    int a, b;
    scanf("%d %d", &a, &b);
    g[a].push_back(b);
    g[b].push_back(a);
  }
  int ind = 0;
  for (int i = 1; i <= N; i++) {
    if (!seen[i]) {
      dfs(i, ind);
      ind++;
    }
  }
  ans = N;
  int k = ind;
  // Angus's solution to Mexican Wave, modified
  {
    int i = 0;
    for (int j = 0; j < N; j++) {
      if (grp[j] < k) {
        if (!num[grp[j]]) tot++;
        num[grp[j]]++;
      }
      while (tot == k) {
        if (grp[i] < k) {
          num[grp[i]]--;
          if (!num[grp[i]]) tot--;
        }
        i++;
      }
      //printf("%d %d\n", i, j);
      if (i > 0) {
        ans = min(ans, j - i + 2);
      }
    }
  }
  printf("%d\n", ans);
}
