#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if(!(cin >> n)) return 0;
    vector<pair<int,int>> moves;
    moves.reserve((1u<<n) - 1);
    function<void(int,int,int,int)> hanoi = [&](int n, int s, int m, int e){
        if(n == 0) return;
        hanoi(n-1, s, e, m);
        moves.push_back({s, e});
        hanoi(n-1, m, s, e);
    };
    hanoi(n, 1, 2, 3);
    cout << moves.size() << '\n';
    for(auto& [a, b] : moves) cout << a << ' ' << b << '\n';
    return 0;
}