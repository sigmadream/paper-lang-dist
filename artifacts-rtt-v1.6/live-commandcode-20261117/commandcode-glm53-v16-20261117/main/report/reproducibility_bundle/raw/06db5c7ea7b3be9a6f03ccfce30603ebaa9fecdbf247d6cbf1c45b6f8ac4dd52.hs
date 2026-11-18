import qualified Data.IntSet as S
pairs (a:b:xs) = (a,b) : (b,a) : pairs xs
pairs _ = []
main = do
  (_:m:xs) <- fmap (map read . words) getContents :: IO [Int]
  let edges = pairs (take (2*m) xs)
      direct = S.fromList [b | (a,b) <- edges, a==1]
      two = S.fromList [b | (a,b) <- edges, S.member a direct]
  print (S.size (S.delete 1 (S.union direct two)))
