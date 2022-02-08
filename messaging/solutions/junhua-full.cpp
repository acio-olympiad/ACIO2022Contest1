#include <iostream>
#include <set>
#include <utility>
#define MAXN 100005
using namespace std;

class DSU {
    int Set[MAXN];
public:
    int Find(int x) {return Set[x] == x ? x : Set[x]=Find(Set[x]);}
    void Union(int x, int y) {Set[Find(x)]=Find(y);}
    void Init(int n) {for (int i=1; i<=n; i++) {Set[i]=i;}}
} UF;

int N, M;
int color[MAXN], last[MAXN], isrep[MAXN], numreps;
set <pair<int,int> > PQ; //lmao
int main() {
    //freopen("rangein.txt","r",stdin);
    scanf("%d %d",&N,&M);
    UF.Init(N);
    for (int i=0; i<M; i++) {
        int u,v;
        scanf("%d %d",&u,&v);
        UF.Union(u,v);
    }
    for (int i=1; i<=N; i++) {
        color[i] = UF.Find(i);
        if (!isrep[color[i]]) {numreps++;}
        isrep[color[i]] = 1;

    }

    int best = 1<<30;
    for (int i=1; i<=N; i++) {
        auto ptr = PQ.find({last[color[i]], color[i]});
        if (ptr != PQ.end()) {PQ.erase(ptr);}
        PQ.insert({i, color[i]});
        last[color[i]] = i;
        if (PQ.size() == numreps) {
            best = min(best, i-(*PQ.begin()).first+1);
        }
    }
    cout << best;
}
