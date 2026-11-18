import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static void solve() throws Exception {int n=nextInt();StringBuilder out=new StringBuilder();for(int i=0;i<n;i++){String s=next();int depth=0;for(int j=0;j<s.length();j++){depth+=s.charAt(j)=='('?1:-1;if(depth<0)break;}out.append(depth==0?"YES\n":"NO\n");}System.out.print(out);}
}
