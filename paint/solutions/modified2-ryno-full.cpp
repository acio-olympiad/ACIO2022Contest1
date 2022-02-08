/* N <= 2e3, K <= 2e3

fracturing search
O(NK log NK)
*/

#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
#include <assert.h>
using namespace std;
typedef long long ll;

ll N, K, D;
vector<ll> costs[2005];
vector<ll> prevUsed[2005];
struct State {
    // used is represented by prevUsed[i]
    ll i;
    // modify day `d`, if d == -1 dont modify
    ll d = -1;
    // what to increment it to. if itemI == costs[d].size(), then remove this day
    ll itemI = -1;

    // updated stats
    ll numItems, cost = 0;
    ll hasChoice;

    // day is discarded when used[d] = cost[d].size()
    bool operator<(State o) const {
        if (numItems == o.numItems) return cost > o.cost;
        return numItems < o.numItems;
    }

    vector<ll> applyUpdate() {
        vector<ll> used = prevUsed[i];
        if (d != -1) used[d] = itemI;
        return used;
    }
};
priority_queue<State> pq;

State initState() {
    State output;
    prevUsed[0].resize(D + 1);
    output.i = 0;
    
    output.numItems = D;
    for (ll d = 0; d < D; ++d) output.cost += costs[d][0];
    output.hasChoice = 0;
    
    return output;
}

void fracturingSearch() {
    pq.push(initState());

    for (ll i = 0; i < K - 1; ++i) {
        State curr = pq.top();
        pq.pop();
        
        // apply update, store in prevUsed[i]
        prevUsed[i] = curr.applyUpdate();

        // find children
        for (ll d = curr.hasChoice; d < D; ++d) {
            // option 1: increment the cost
            for (ll itemI = prevUsed[i][d] + 1; itemI < (ll)costs[d].size(); ++itemI) {
                State neighbour;
                neighbour.i = i;
                neighbour.d = d;
                neighbour.itemI = itemI;

                neighbour.cost = curr.cost + costs[d][itemI] - costs[d][prevUsed[i][d]];
                neighbour.numItems = curr.numItems;
                neighbour.hasChoice = d + 1;
                pq.push(neighbour);
            }

            // option 2: remove this day
            if (prevUsed[i][d] != (ll)costs[d].size()) {
                State neighbour;
                neighbour.i = i;
                neighbour.d = d;
                neighbour.itemI = costs[d].size();

                neighbour.cost = curr.cost - costs[d][prevUsed[i][d]];
                neighbour.numItems = curr.numItems - 1;
                neighbour.hasChoice = d + 1;
                pq.push(neighbour);
            }
        }
    }

    cout << pq.top().numItems << " " << pq.top().cost << "\n";
}

int main() {
    cin.tie(0); ios::sync_with_stdio(0);

    cin >> N >> K >> D;
    for (ll d, w, i = 0; i < N; ++i) {
        cin >> d >> w;
        --d;
        costs[d].push_back(w);
    }
    for (ll d = 0; d < D; ++d) sort(costs[d].begin(), costs[d].end());

    fracturingSearch();
}
