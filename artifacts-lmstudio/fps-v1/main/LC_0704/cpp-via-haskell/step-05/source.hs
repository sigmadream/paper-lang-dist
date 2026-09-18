module Main where

binarySearch :: Int -> Int -> Int -> [Int] -> Int
binarySearch lo hi target a = go lo hi
  where
    go l h
      | l < h     = let mid = l + (h - l) `div` 2
                    in if a !! mid < target then go (mid + 1) h else go l mid
      | otherwise = if l == length a || a !! l /= target then -1 else l

main :: IO ()
main = do
  [n, target] <- map read . words <$> getLine
  a <- map read . words <$> getLine
  print $ binarySearch 0 n target a