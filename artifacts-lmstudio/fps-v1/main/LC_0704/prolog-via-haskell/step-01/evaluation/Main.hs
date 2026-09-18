import Data.List (splitAt)
import System.IO

binarySearch :: Ord a => a -> [a] -> Int
binarySearch target xs = go 0 (length xs - 1)
  where
    go l h | l > h     = -1
    go l h = let m = l + (h - l) `div` 2
              in case compare (xs !! m) target of
                   EQ -> m
                   LT -> go (m + 1) h
                   GT -> go l (m - 1)

main :: IO ()
main = do
  [n, t] <- map read . words <$> getLine
  xs <- map read . words <$> getLine
  print $ binarySearch t xs