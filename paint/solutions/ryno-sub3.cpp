/* N <= 18

brute force through all valid options
O(N 2^N)
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
pair<ll, ll> costs[200005];
vector<pair<ll, ll>> bests;
bool seen[(1 << 20) + 5];

int main() {
    cin.tie(0); ios::sync_with_stdio(0);
    cin >> N >> K >> D;
    for (ll i = 0; i < N; ++i) cin >> costs[i].first >> costs[i].second;

    for (ll bits = 0; bits < (1ll << N); ++bits) {
        ll daySeen = 0;
        ll numDays = 0, total = 0;
        ll trueBits = 0;
        for (ll i = 0; i < N; ++i) {
            if ((bits & (1ll << i)) && !(daySeen & (1ll << costs[i].first))) {
                daySeen |= 1ll << costs[i].first;
                total += costs[i].second;
                ++numDays;
                trueBits |= 1ll << i;
            }
        }

        if (!seen[trueBits]) {
            seen[trueBits] = true;
            bests.push_back({ -numDays, total });
        }
    }
    
    sort(bests.begin(), bests.end());
    cout << -bests[K - 1].first << " " << bests[K - 1].second << "\n";
}
