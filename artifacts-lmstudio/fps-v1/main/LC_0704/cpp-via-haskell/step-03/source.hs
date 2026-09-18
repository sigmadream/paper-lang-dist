module Main where

binarySearch :: Int -> Int -> Int -> [Int] -> Int
binarySearch lo hi target a
  | lo < hi   = let mid = lo + (hi - lo) `div` 2
                in if a !! mid < target then binarySearch (mid + 1) hi target a else binarySearch lo mid target a
  | otherwise = if lo == length a || a !! lo /= target then -1 else lo

main :: IO ()
main = do
  [n, target] <- map read . words <$> getLine
  a <- map read . words <$> getLine
  print $ binarySearch 0 n target a