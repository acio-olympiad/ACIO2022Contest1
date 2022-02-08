/* K = 1

greedy algorithm - take as many cuts as possible, and take the cheapest beef of each cut
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

int main() {
    cin.tie(0); ios::sync_with_stdio(0);
    cin >> N >> K >> D;
    for (ll d, w, i = 0; i < N; ++i) {
        cin >> d >> w;
        costs[d].push_back(w);
    }

    ll total = 0;
    for (ll d = 1; d <= D; ++d) {
        total += *min_element(costs[d].begin(), costs[d].end());
    }
    cout << D << " " << total << "\n";
}
