#include <iostream>
#include <string>
using namespace std;

bool isPalindrome(const string& s, int left, int right) {
    while (left < right) {
        if (s[left] != s[right]) return false;
        ++left;
        --right;
    }
    return true;
}

int main() {
    string s;
    cin >> s;
    cout << (isPalindrome(s, 0, s.size() - 1) ? 1 : 0) << endl;
    return 0;
}