import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.nextLine();
        String bomb = scanner.nextLine();
        scanner.close();
        
        String res = "";
        int b_len = bomb.length();
        
        for (char c : s.toCharArray()) {
            res += c;
            if (res.length() >= b_len) {
                boolean match = true;
                for (int i = 0; i < b_len; i++) {
                    if (res.charAt(res.length() - b_len + i) != bomb.charAt(i)) {
                        match = false;
                        break;
                    }
                }
                if (match) {
                    res = res.substring(0, res.length() - b_len);
                }
            }
        }
        
        if (res.isEmpty()) System.out.println("FRULA");
        else System.out.println(res);
    }
}
