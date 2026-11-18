module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)

readInts :: IO [Int]
readInts = do
  s <- BS.getContents
  return $ map (fst . fromJust' . BS.readInt) (BS.words s)
  where
    fromJust' (Just x) = x
    fromJust' Nothing = error "bad input"

feasible :: [Int] -> Int -> Int -> Bool
feasible a mid c = go (tail a) (head a) 1
  where
    go [] _ cnt = cnt >= c
    go (x:xs) prev cnt
      | x - prev >= mid = go xs x (cnt + 1)
      | otherwise = go xs prev cnt

binarySearch :: [Int] -> Int -> Int -> Int -> Int -> Int
binarySearch a lo hi c ans
  | lo > hi = ans
  | feasible a mid c = binarySearch a (mid + 1) hi c mid
  | otherwise = binarySearch a lo (mid - 1) c ans
  where
    mid = lo + (hi - lo) `div` 2

main :: IO ()
main = do
  xs <- readInts
  case xs of
    (n:c:rest) -> do
      let a = take n rest
          s = sort a
          lo = 1
          hi = last s - head s
          ans = binarySearch s lo hi c 0
      print ans
    _ -> return ()