import java.io.*;

public class Main {
    private static boolean isTrimChar(char c) {
        return c <= ' ';
    }

    private static boolean isCppSpaceAscii(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\u000B'
                || c == '\f' || c == '\r';
    }

    private static Integer parseJavaInt(String s) {
        if (s.isEmpty()) return null;

        int i = 0;
        boolean neg = false;

        if (s.charAt(i) == '+' || s.charAt(i) == '-') {
            neg = s.charAt(i) == '-';
            ++i;
            if (i == s.length()) return null;
        }

        long v = 0;
        long limit = neg ? 2147483648L : 2147483647L;

        for (; i < s.length(); ++i) {
            char c = s.charAt(i);
            if (c < '0' || c > '9') return null;

            int d = c - '0';
            if (v > (limit - d) / 10) return null;
            v = v * 10 + d;
        }

        if (neg) {
            if (v == 2147483648L) return Integer.MIN_VALUE;
            return (int) -v;
        } else {
            return (int) v;
        }
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;

        int start = 0;
        int end = line.length();

        while (start < end && isTrimChar(line.charAt(start))) ++start;
        while (end > start && isTrimChar(line.charAt(end - 1))) --end;

        String trimmed = line.substring(start, end);
        if (trimmed.isEmpty()) return;

        int tokenEnd = 0;
        while (tokenEnd < trimmed.length() && !isCppSpaceAscii(trimmed.charAt(tokenEnd))) {
            ++tokenEnd;
        }

        String token = trimmed.substring(0, tokenEnd);
        Integer parsed = parseJavaInt(token);
        if (parsed == null) return;

        int n = parsed;
        if (n < 0) return;

        int[] counts = new int[n + 1];
        for (int i = 1; i <= n; ++i) {
            counts[i] = counts[i / 2] + (i % 2);
        }

        StringBuilder output = new StringBuilder((n + 1) * 7);
        for (int i = 0; i <= n; ++i) {
            if (i > 0) output.append(' ');
            output.append(counts[i]);
        }
        output.append('\n');

        System.out.print(output.toString());
    }
}