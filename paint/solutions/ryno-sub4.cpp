/* the number of items = D, total cost <= 2e3

knapsack over c_i, also record the frequency of each possible knapsack value
make sure at only 1 beef is taken of each cut
O(N * total cost)
*/

#include <algorithm>
#include <iostream>
#include <vector>
#include <set>
#include <numeric>
#include <fstream>
using namespace std;
typedef long long ll;

ll N, K, D;
vector<ll> costs[2005];
ll knapsack[2005], newKnapsack[2005];

int main() {
    cin.tie(0); ios::sync_with_stdio(0);
    cin >> N >> K >> D;
    for (ll d, w, i = 0; i < N; ++i) {
        cin >> d >> w;
        costs[d].push_back(w);
    }

    knapsack[0] = 1;
    for (ll d = 1; d <= D; ++d) {
        fill(begin(newKnapsack), end(newKnapsack), 0ll);
        for (ll cost : costs[d]) {
            for (ll prevCost = 0; prevCost + cost <= 2e3; ++prevCost) {
                newKnapsack[prevCost + cost] = min(1000000000LL, newKnapsack[prevCost + cost] + knapsack[prevCost]);
            }
        }
        copy(begin(newKnapsack), end(newKnapsack), begin(knapsack));
    }

    ll cost = 0;
    for (ll sum = 1; sum <= K; sum += knapsack[cost]) {
        ++cost;
    }
    cout << D << " " << cost << "\n";
}
