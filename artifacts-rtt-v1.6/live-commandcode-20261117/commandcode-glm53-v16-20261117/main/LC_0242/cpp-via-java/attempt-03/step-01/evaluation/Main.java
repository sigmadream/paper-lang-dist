import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StreamTokenizer st = new StreamTokenizer(br);
        st.ordinaryChars(33, 126);
        st.wordChars('a', 'z');
        String s = (st.nextToken() == StreamTokenizer.TT_WORD) ? st.sval : "";
        String t = (st.nextToken() == StreamTokenizer.TT_WORD) ? st.sval : "";
        int[] counts = new int[26];
        for (char c : s.toCharArray()) counts[c - 'a']++;
        for (char c : t.toCharArray()) counts[c - 'a']--;
        boolean ok = true;
        for (int x : counts) if (x != 0) { ok = false; break; }
        System.out.println(ok ? 1 : 0);
    }
}