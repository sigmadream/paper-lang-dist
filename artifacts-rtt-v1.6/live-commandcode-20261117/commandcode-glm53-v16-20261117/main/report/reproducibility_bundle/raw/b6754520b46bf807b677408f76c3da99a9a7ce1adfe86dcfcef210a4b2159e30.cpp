#include <iostream>
#include <string>
#include <sstream>
using namespace std;

int main() {
    long long A, B;
    if (!(cin >> A >> B)) return 0;
    long long a = A, b = B;
    while (b) { long long r = a % b; a = b; b = r; }
    long long g = a;
    cout << g << "\n" << A / g * B << "\n";
    return 0;
}