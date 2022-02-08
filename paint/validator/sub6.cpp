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

struct State {
    ll numItems = 0, cost = 0;
    ll hasChoice;
    ll lastChoice;
    // choices[i] <= used[i]
    // day is discarded when used[d] = choices[d] = cost[d].size()
    // day has free choice when choices[d] = -1

    bool operator<(State o) const {
        if (numItems == o.numItems) return cost > o.cost;
        return numItems < o.numItems;
    }
};
priority_queue<State> pq;

State initState() {
    State output;
    output.numItems = D;
    for (ll d = 1; d <= D; ++d) output.cost += costs[d][0];
    output.hasChoice = 1;
    //output.used.resize(D + 1);

    return output;
}

void fracturingSearch() {
    pq.push(initState());

    for (ll rep = 0; rep < K - 1; ++rep) {
        State curr = pq.top();
        pq.pop();

        for (ll d = curr.hasChoice; d <= D; ++d) {
            //cerr << "d " << d << "\n";
            //cerr << "PQ size: " << pq.size() << "\n";
            // option 1: increment the cost
            for (ll itemI = 1; itemI < (ll)costs[d].size(); ++itemI) {
                State neighbour = curr;
                neighbour.cost += costs[d][itemI] - costs[d][0];
                neighbour.hasChoice = d + 1;
                //neighbour.used[d] = itemI;
                pq.push(neighbour);
            }

            // option 2: remove this day
            if (0 != (ll)costs[d].size()) {
                State neighbour = curr;
                neighbour.cost -= costs[d][0];
                neighbour.numItems--;
                neighbour.hasChoice = d + 1;
                //neighbour.used[d] = costs[d].size();
                pq.push(neighbour);
            }
        }
    }

    cout << pq.top().numItems << " " << pq.top().cost << "\n";
}

int main() {
    cin.tie(0); ios::sync_with_stdio(0);

    cin >> N >> K >> D;
    assert(1 <= N && N <= 2000);
    assert(1 <= K && K <= 2000);
    assert(1 <= D && D <= N);
    for (ll d, w, i = 0; i < N; ++i) {
        cin >> d >> w;
        assert(1 <= d && d <= D);
        assert(1 <= w && w <= 1000000000);
        costs[d].push_back(w);
    }
    for (ll d = 1; d <= D; ++d) sort(costs[d].begin(), costs[d].end());

    fracturingSearch();
}
