#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

static bool isSpaceChar(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f';
}

static string trimJava(const string &s) {
    int begin = 0;
    int end = static_cast<int>(s.size());
    while (begin < end && s[begin] <= ' ') ++begin;
    while (end > begin && s[end - 1] <= ' ') --end;
    return s.substr(begin, end - begin);
}

static bool parseJavaInt(const string &s, int &out) {
    if (s.empty()) return false;

    int i = 0;
    bool negative = false;
    char c0 = s[0];

    if (c0 == '+' || c0 == '-') {
        negative = (c0 == '-');
        ++i;
        if (i == static_cast<int>(s.size())) return false;
    }

    long long value = 0;
    long long limit = negative ? 2147483648LL : 2147483647LL;

    for (; i < static_cast<int>(s.size()); ++i) {
        char c = s[i];
        if (c < '0' || c > '9') return false;
        value = value * 10 + (c - '0');
        if (value > limit) return false;
    }

    out = static_cast<int>(negative ? -value : value);
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string firstLine;
    if (!getline(cin, firstLine)) return 0;

    firstLine = trimJava(firstLine);
    if (firstLine.empty()) return 0;

    int pos = 0;
    while (pos < static_cast<int>(firstLine.size()) && !isSpaceChar(firstLine[pos])) {
        ++pos;
    }

    string firstToken = firstLine.substr(0, pos);
    int n;
    if (!parseJavaInt(firstToken, n)) return 0;
    if (n < 0) return 0;

    vector<int> a(n);
    int count = 0;

    string line;
    while (count < n && getline(cin, line)) {
        int i = 0;
        int len = static_cast<int>(line.size());

        while (i < len && count < n) {
            while (i < len && isSpaceChar(line[i])) ++i;
            if (i >= len) break;

            int start = i;
            while (i < len && !isSpaceChar(line[i])) ++i;

            string token = line.substr(start, i - start);
            int value;
            if (!parseJavaInt(token, value)) value = 0;

            a[count++] = value;
        }
    }

    while (count < n) {
        a[count++] = 0;
    }

    int write = 0;
    for (int read = 0; read < n; ++read) {
        if (a[read] != 0) {
            swap(a[write], a[read]);
            ++write;
        }
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) cout << ' ';
        cout << a[i];
    }
    cout << '\n';

    return 0;
}