import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {int m=nextInt(),n=nextInt();java.math.BigInteger[] row=new java.math.BigInteger[n];Arrays.fill(row,java.math.BigInteger.ONE);for(int i=1;i<m;i++)for(int j=1;j<n;j++)row[j]=row[j].add(row[j-1]);System.out.println(row[n-1]);}
}
