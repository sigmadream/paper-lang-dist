import os

base_dir = r"c:\Users\sigma\works\paper-lang-dist\corpus\solutions"

codes = {
    "11729": r"""#include <iostream>
#include <vector>

using namespace std;

void hanoi(int n, int start, int mid, int end, vector<pair<int, int>>& moves) {
    if (n == 1) {
        moves.push_back({start, end});
        return;
    }
    hanoi(n - 1, start, end, mid, moves);
    moves.push_back({start, end});
    hanoi(n - 1, mid, start, end, moves);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<pair<int, int>> moves;
    hanoi(n, 1, 2, 3, moves);
    cout << moves.size() << "\n";
    for (auto& p : moves) {
        cout << p.first << " " << p.second << "\n";
    }
    return 0;
}
""",
    "1992": r"""#include <iostream>
#include <vector>
#include <string>

using namespace std;

string solve(const vector<string>& grid, int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;
    for (int i = r; i < r + size; i++) {
        for (int j = c; j < c + size; j++) {
            if (grid[i][j] != first) {
                same = false;
                break;
            }
        }
        if (!same) break;
    }
    
    if (same) return string(1, first);
    
    int half = size / 2;
    string tl = solve(grid, r, c, half);
    string tr = solve(grid, r, c + half, half);
    string bl = solve(grid, r + half, c, half);
    string br = solve(grid, r + half, c + half, half);
    
    return "(" + tl + tr + bl + br + ")";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    vector<string> grid(n);
    for (int i = 0; i < n; i++) cin >> grid[i];
    cout << solve(grid, 0, 0, n) << "\n";
    return 0;
}
""",
    "9935": r"""#include <iostream>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string s, bomb;
    if (!(cin >> s >> bomb)) return 0;
    
    string res = "";
    int b_len = bomb.length();
    
    for (char c : s) {
        res += c;
        if (res.length() >= b_len) {
            bool match = true;
            for (int i = 0; i < b_len; i++) {
                if (res[res.length() - b_len + i] != bomb[i]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                for (int i = 0; i < b_len; i++) res.pop_back();
            }
        }
    }
    
    if (res.empty()) cout << "FRULA\n";
    else cout << res << "\n";
    return 0;
}
""",
    "10988": r"""#include <iostream>
#include <string>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string s;
    if (!(cin >> s)) return 0;
    
    bool valid = true;
    for (int i = 0; i < s.length() / 2; i++) {
        if (s[i] != s[s.length() - 1 - i]) {
            valid = false;
            break;
        }
    }
    cout << (valid ? 1 : 0) << "\n";
    return 0;
}
""",
    "9012": r"""#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    if (!(cin >> t)) return 0;
    while (t--) {
        string s;
        cin >> s;
        int bal = 0;
        bool valid = true;
        for (char c : s) {
            if (c == '(') bal++;
            else bal--;
            if (bal < 0) {
                valid = false;
                break;
            }
        }
        if (bal != 0) valid = false;
        cout << (valid ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
    "1929": r"""#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int m, n;
    if (!(cin >> m >> n)) return 0;
    
    vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    
    for (int i = 2; i * i <= n; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }
    
    for (int i = m; i <= n; i++) {
        if (is_prime[i]) cout << i << "\n";
    }
    return 0;
}
""",
    "2609": r"""#include <iostream>

using namespace std;

int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int a, b;
    if (!(cin >> a >> b)) return 0;
    int g = gcd(a, b);
    cout << g << "\n" << (a / g) * b << "\n";
    return 0;
}
""",
    "1158": r"""#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, k;
    if (!(cin >> n >> k)) return 0;
    
    vector<int> q;
    for (int i = 1; i <= n; i++) q.push_back(i);
    
    cout << "<";
    int idx = 0;
    while (!q.empty()) {
        idx = (idx + k - 1) % q.size();
        cout << q[idx];
        q.erase(q.begin() + idx);
        if (!q.empty()) cout << ", ";
    }
    cout << ">\n";
    return 0;
}
""",
    "14719": r"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int h, w;
    if (!(cin >> h >> w)) return 0;
    
    vector<int> a(w);
    for (int i = 0; i < w; i++) cin >> a[i];
    
    int ans = 0;
    for (int i = 1; i < w - 1; i++) {
        int left_max = 0, right_max = 0;
        for (int j = 0; j <= i; j++) left_max = max(left_max, a[j]);
        for (int j = i; j < w; j++) right_max = max(right_max, a[j]);
        int bound = min(left_max, right_max);
        if (bound > a[i]) ans += bound - a[i];
    }
    
    cout << ans << "\n";
    return 0;
}
""",
    "1260": r"""#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

void dfs(int cur, const vector<vector<int>>& adj, vector<bool>& vis) {
    vis[cur] = true;
    cout << cur << " ";
    for (int nxt : adj[cur]) {
        if (!vis[nxt]) dfs(nxt, adj, vis);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, m, v;
    if (!(cin >> n >> m >> v)) return 0;
    
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    for (int i = 1; i <= n; i++) sort(adj[i].begin(), adj[i].end());
    
    vector<bool> vis(n + 1, false);
    dfs(v, adj, vis);
    cout << "\n";
    
    fill(vis.begin(), vis.end(), false);
    queue<int> q;
    q.push(v);
    vis[v] = true;
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        cout << cur << " ";
        for (int nxt : adj[cur]) {
            if (!vis[nxt]) {
                vis[nxt] = true;
                q.push(nxt);
            }
        }
    }
    cout << "\n";
    return 0;
}
""",
    "9663": r"""#include <iostream>
#include <vector>

using namespace std;

int ans = 0;
int n;
vector<bool> col, diag1, diag2;

void solve(int r) {
    if (r == n) {
        ans++;
        return;
    }
    for (int c = 0; c < n; c++) {
        if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = true;
        solve(r + 1);
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = false;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    if (!(cin >> n)) return 0;
    
    col.assign(n, false);
    diag1.assign(2 * n - 1, false);
    diag2.assign(2 * n - 1, false);
    solve(0);
    
    cout << ans << "\n";
    return 0;
}
""",
    "9251": r"""#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    string a, b;
    if (!(cin >> a >> b)) return 0;
    
    int n = a.length();
    int m = b.length();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (a[i - 1] == b[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
            else dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    
    cout << dp[n][m] << "\n";
    return 0;
}
""",
    "1620": r"""#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <cctype>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, m;
    if (!(cin >> n >> m)) return 0;
    
    unordered_map<string, int> name_to_id;
    vector<string> id_to_name(n + 1);
    
    for (int i = 1; i <= n; i++) {
        string name;
        cin >> name;
        name_to_id[name] = i;
        id_to_name[i] = name;
    }
    
    for (int i = 0; i < m; i++) {
        string q;
        cin >> q;
        if (isdigit(q[0])) {
            cout << id_to_name[stoi(q)] << "\n";
        } else {
            cout << name_to_id[q] << "\n";
        }
    }
    return 0;
}
""",
    "2003": r"""#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    long long m;
    if (!(cin >> n >> m)) return 0;
    
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    int ans = 0;
    long long sum = 0;
    int end = 0;
    
    for (int start = 0; start < n; start++) {
        while (sum < m && end < n) {
            sum += a[end];
            end++;
        }
        if (sum == m) ans++;
        sum -= a[start];
    }
    
    cout << ans << "\n";
    return 0;
}
""",
    "18870": r"""#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (!(cin >> n)) return 0;
    
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    
    vector<int> sorted_a = a;
    sort(sorted_a.begin(), sorted_a.end());
    sorted_a.erase(unique(sorted_a.begin(), sorted_a.end()), sorted_a.end());
    
    for (int i = 0; i < n; i++) {
        int compressed = lower_bound(sorted_a.begin(), sorted_a.end(), a[i]) - sorted_a.begin();
        cout << compressed << " ";
    }
    cout << "\n";
    return 0;
}
"""
}

count = 0
for pid, code in codes.items():
    sol_dir = os.path.join(base_dir, f"IPOP_{pid}")
    os.makedirs(sol_dir, exist_ok=True)
    with open(os.path.join(sol_dir, "reference.cpp"), "w", encoding="utf-8") as f:
        f.write(code)
    count += 1
print(f"총 {count}개의 C++ reference.cpp 솔루션 파일을 생성했습니다.")
