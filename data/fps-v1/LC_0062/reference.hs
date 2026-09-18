import Data.Array
main = do
  [m,n] <- fmap (map read . words) getContents :: IO [Int]
  let table = array ((1,1),(m,n)) [((i,j), value i j) | i <- [1..m], j <- [1..n]]
      value 1 _ = 1 :: Integer
      value _ 1 = 1
      value i j = table!(i-1,j) + table!(i,j-1)
  print (table!(m,n))
