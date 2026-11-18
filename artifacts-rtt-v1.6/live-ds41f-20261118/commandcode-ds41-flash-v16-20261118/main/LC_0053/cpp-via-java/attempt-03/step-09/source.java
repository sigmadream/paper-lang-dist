import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        if (!sc.hasNext()) return;

        String ns = sc.next();
        int n;
        try {
            n = Integer.parseInt(ns);
        } catch (Exception e) {
            return;
        }

        if (!sc.hasNext()) return;

        String firstToken = sc.next();
        long first;
        try {
            first = Long.parseLong(firstToken);
        } catch (Exception e) {
            return;
        }

        long cur = first;
        long best = first;

        for (int i = 1; i < n; i++) {
            if (!sc.hasNext()) break;

            String token = sc.next();
            long x;
            try {
                x = Long.parseLong(token);
            } catch (Exception e) {
                break;
            }

            cur = Math.max(x, cur + x);
            best = Math.max(best, cur);
        }

        System.out.println(best);
    }
}