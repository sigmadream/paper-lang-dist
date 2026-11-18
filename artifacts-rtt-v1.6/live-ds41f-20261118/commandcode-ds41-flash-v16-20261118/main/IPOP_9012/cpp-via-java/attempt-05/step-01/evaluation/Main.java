import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) return;
        int t = sc.nextInt();
        StringBuilder sb = new StringBuilder();
        while (t-- > 0) {
            String s = sc.next();
            int bal = 0;
            boolean valid = true;
            for (int i = 0; i < s.length(); i++) {
                char c = s.charAt(i);
                if (c == '(') bal++;
                else bal--;
                if (bal < 0) {
                    valid = false;
                    break;
                }
            }
            if (bal != 0) valid = false;
            sb.append(valid ? "YES" : "NO").append('\n');
        }
        System.out.print(sb);
    }
}