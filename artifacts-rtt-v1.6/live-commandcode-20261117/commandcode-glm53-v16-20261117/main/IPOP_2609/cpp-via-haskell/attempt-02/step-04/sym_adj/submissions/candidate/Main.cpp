#include <iostream>
#include <numeric>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    long long g = std::gcd(a, b);
    cout << g << "\n" << a / g * b << "\n";
    return 0;
}