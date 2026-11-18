import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {String a=next(),b=next();int[] counts=new int[26];for(char c:a.toCharArray())counts[c-'a']++;for(char c:b.toCharArray())counts[c-'a']--;for(int count:counts)if(count!=0){System.out.println(0);return;}System.out.println(1);}
}
