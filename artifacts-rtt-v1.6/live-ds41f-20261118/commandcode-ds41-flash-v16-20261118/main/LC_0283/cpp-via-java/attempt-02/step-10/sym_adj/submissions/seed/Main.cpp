#include <bits/stdc++.h>
using namespace std;

static bool isSpaceChar(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f';
}

static string trimJava(const string& s) {
    size_t begin = 0;
    size_t end = s.size();

    while (begin < end && static_cast<unsigned char>(s[begin]) <= ' ') ++begin;
    while (end > begin && static_cast<unsigned char>(s[end - 1]) <= ' ') --end;

    return s.substr(begin, end - begin);
}

static bool parseJavaInt(const string& s, int& out) {
    if (s.empty()) return false;

    size_t i = 0;
    bool negative = false;

    if (s[i] == '+' || s[i] == '-') {
        negative = (s[i] == '-');
        ++i;
        if (i == s.size()) return false;
    }

    long long value = 0;
    const long long limit = negative ? 2147483648LL : 2147483647LL;

    for (; i < s.size(); ++i) {
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

    size_t pos = 0;
    while (pos < firstLine.size() && !isSpaceChar(firstLine[pos])) ++pos;

    string firstToken = firstLine.substr(0, pos);
    int n;
    if (!parseJavaInt(firstToken, n)) return 0;

    if (n < 0) return 0;

    vector<int> a(n);
    int count = 0;

    string line;
    while (count < n && getline(cin, line)) {
        size_t i = 0;
        while (i < line.size() && count < n) {
            while (i < line.size() && isSpaceChar(line[i])) ++i;
            if (i >= line.size()) break;

            size_t start = i;
            while (i < line.size() && !isSpaceChar(line[i])) ++i;

            string token = line.substr(start, i - start);
            int value = 0;
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