import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    static int gcd(int a, int b) {
        while (b != 0) {
            int r = a % b;
            a = b;
            b = r;
        }
        return a;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        String[] parts = line.trim().split("\\s+");
        if (parts.length < 2) return;
        int a = Integer.parseInt(parts[0]);
        int b = Integer.parseInt(parts[1]);
        int g = gcd(a, b);
        StringBuilder sb = new StringBuilder();
        sb.append(g).append('\n').append((a / g) * b).append('\n');
        System.out.print(sb);
    }
}