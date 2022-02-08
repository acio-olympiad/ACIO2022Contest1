/* K = 2

find K = 1 using the greedy algorithm from subtask 1
try all modifications to this option:
 - replacements (i want to pay more for this cut)
 - removals (i dont want to buy beef of this cut)
O(N)
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
vector<ll> costs[200005];
vector<ll> modifyOptions, modifyOptions2;

int main() {
    cin.tie(0); ios::sync_with_stdio(0);
    cin >> N >> K >> D;
    for (ll d, w, i = 0; i < N; ++i) {
        cin >> d >> w;
        costs[d].push_back(w);
    }

    ll best = 0;
    for (ll d = 1; d <= D; ++d) {
        sort(costs[d].begin(), costs[d].end());
        best += costs[d][0];
        if (costs[d].size() > 1) modifyOptions.push_back(costs[d][1] - costs[d][0]);
        modifyOptions2.push_back(-costs[d][0]);
    }

    if (!modifyOptions.empty()) {
        cout << D << " " << best + *min_element(modifyOptions.begin(), modifyOptions.end()) << "\n";
    }
    else {
        cout << D - 1 << " " << best + *min_element(modifyOptions2.begin(), modifyOptions2.end()) << "\n";
    }
    
}
