#include <iostream>
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
