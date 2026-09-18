import Data.Array
search array target lo hi
  | lo > hi = -1
  | array!mid == target = mid
  | array!mid < target = search array target (mid+1) hi
  | otherwise = search array target lo (mid-1)
  where mid = (lo+hi) `div` 2
main = do
  (n:target:xs) <- fmap (map read . words) getContents :: IO [Int]
  print (search (listArray (0,n-1) xs) target 0 (n-1))
