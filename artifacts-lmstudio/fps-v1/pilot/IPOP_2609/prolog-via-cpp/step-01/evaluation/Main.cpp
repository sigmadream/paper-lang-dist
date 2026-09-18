#include <iostream>
using namespace std;

int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int A, B;
    cin >> A >> B;
    int GCD = gcd(A, B);
    cout << GCD << endl;
    cout << (A / GCD) * B << endl;
    return 0;
}