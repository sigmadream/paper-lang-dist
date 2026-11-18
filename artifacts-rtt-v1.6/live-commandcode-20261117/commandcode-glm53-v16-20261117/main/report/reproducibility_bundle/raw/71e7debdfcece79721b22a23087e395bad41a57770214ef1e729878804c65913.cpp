#include <bits/stdc++.h>
using namespace std;

int main(){
    int n;
    if(!(cin >> n)) return 0;
    vector<long long> a(n);
    for(auto &x : a) cin >> x;
    int w = 0;
    for(int r = 0; r < n; r++){
        if(a[r] != 0){
            swap(a[w], a[r]);
            w++;
        }
    }
    for(int i = 0; i < n; i++){
        cout << a[i] << " \n"[i+1==n];
    }
    return 0;
}