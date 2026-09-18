import Data.Array
main = do
  values <- fmap (map read . words) getContents :: IO [Int]
  let n = head values
      score = listArray (1,n) (tail values)
      best = listArray (0,n) [value i | i <- [0..n]]
      value 0 = 0
      value 1 = score!1
      value 2 = score!1 + score!2
      value i = max (best!(i-2)) (best!(i-3) + score!(i-1)) + score!i
  print (best!n)
