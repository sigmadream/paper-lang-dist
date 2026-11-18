module Main where

import Data.List (sort)

canPlace :: Int -> Int -> [Int] -> Bool
canPlace _ _ [] = False
canPlace c d (x:xs) = go 1 x xs
  where
    go count _ [] = count >= c
    go count prev (y:ys)
      | y - prev >= d = go (count + 1) y ys
      | otherwise     = go count prev ys

binarySearch :: Int -> Int -> Int -> [Int] -> Int -> Int
binarySearch lo hi ans arr c
  | lo > hi = ans
  | otherwise =
      let mid = lo + (hi - lo) `div` 2
      in if canPlace c mid arr
           then binarySearch (mid + 1) hi mid arr c
           else binarySearch lo (mid - 1) ans arr c

main :: IO ()
main = do
  input <- getContents
  let vals = map read (words input) :: [Int]
  case vals of
    (n:c:rest) -> do
      let arr = sort (take n rest)
          lo = 1
          hi = last arr - head arr
          ans = binarySearch lo hi 0 arr c
      print ans
    _ -> return ()