#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    array<int,26> a{}, b{};
    for(char c : s) a[c-'a']++;
    for(char c : t) b[c-'a']++;
    cout << (a==b ? 1 : 0) << "\n";
    return 0;
}