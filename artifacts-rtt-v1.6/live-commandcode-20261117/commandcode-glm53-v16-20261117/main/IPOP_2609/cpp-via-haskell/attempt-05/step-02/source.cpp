#include <iostream>
#include <string>
#include <sstream>

using namespace std;

long long gcd_(long long a, long long b) {
    while (b != 0) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    istringstream iss(line);
    long long a, b;
    if (iss >> a >> b) {
        long long g = gcd_(a, b);
        cout << g << "\n" << (a / g) * b << "\n";
    }
    return 0;
}