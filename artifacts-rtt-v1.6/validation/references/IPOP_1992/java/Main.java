import java.io.*;
import java.util.*;
public class Main {
static final BufferedInputStream input = new BufferedInputStream(System.in);
static String next() throws Exception {StringBuilder word=new StringBuilder();int c;do{c=input.read();}while(c<=32 && c!=-1);while(c>32 && c!=-1){word.append((char)c);c=input.read();}return word.toString();}
static int nextInt() throws Exception {return Integer.parseInt(next());}
public static void main(String[] args) throws Exception {solve();}
static String[] grid;
static String encode(int r,int c,int size){char first=grid[r].charAt(c);boolean same=true;
for(int i=r;i<r+size;i++)for(int j=c;j<c+size;j++)if(grid[i].charAt(j)!=first)same=false;
if(same)return Character.toString(first);int h=size/2;
return "("+encode(r,c,h)+encode(r,c+h,h)+encode(r+h,c,h)+encode(r+h,c+h,h)+")";}
static void solve() throws Exception {int n=nextInt();grid=new String[n];for(int i=0;i<n;i++)grid[i]=next();System.out.println(encode(0,0,n));}
}
