import java.util.Scanner;
import java.util.LinkedList;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int k = scanner.nextInt();
        
        LinkedList<Integer> queue = new LinkedList<>();
        for (int i = 1; i <= n; i++) {
            queue.add(i);
        }
        
        System.out.print("<");
        int idx = 0;
        while (!queue.isEmpty()) {
            idx = (idx + k - 1) % queue.size();
            System.out.print(queue.remove(idx));
            if (!queue.isEmpty()) {
                System.out.print(", ");
            }
        }
        System.out.println(">");
    }
}
