module Main where

search :: [Int] -> Int -> Int -> Int -> Int
search array target lo hi
  | lo > hi     = -1
  | otherwise   = let mid = (lo + hi) `div` 2
                  in if array !! mid == target then mid
                     else if array !! mid < target then search array target (mid + 1) hi
                     else search array target lo (mid - 1)

main :: IO ()
main = do
  [n, target] <- map read . words <$> getLine
  xs <- map read . words <$> getLine
  print $ search xs target 0 (n - 1)