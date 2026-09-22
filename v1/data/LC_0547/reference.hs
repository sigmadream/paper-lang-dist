import Data.Array
import qualified Data.IntSet as S
visit graph [] seen = seen
visit graph (v:todo) seen
  | S.member v seen = visit graph todo seen
  | otherwise = visit graph (graph!v ++ todo) (S.insert v seen)
components graph [] seen = 0
components graph (v:vs) seen
  | S.member v seen = components graph vs seen
  | otherwise = 1 + components graph vs (visit graph [v] seen)
main = do
  values <- fmap (map read . words) getContents :: IO [Int]
  let n = head values
      matrix = listArray ((0,0),(n-1,n-1)) (tail values)
      graph = listArray (0,n-1) [[j | j <- [0..n-1], matrix!(i,j)==1] | i <- [0..n-1]]
  print (components graph [0..n-1] S.empty :: Int)
