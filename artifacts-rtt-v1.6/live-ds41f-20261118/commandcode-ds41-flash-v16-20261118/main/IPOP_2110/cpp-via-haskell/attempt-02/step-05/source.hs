module Main where

import Data.List (sort)

canPlace :: [Int] -> Int -> Int -> Bool
canPlace [] _ _ = False
canPlace (firstHouse:rest) c d = go rest firstHouse 1
  where
    go [] _ count = count >= c
    go (x:xs) prev count
      | x - prev >= d =
          let newCount = count + 1
          in if newCount >= c
                then True
                else go xs x newCount
      | otherwise = go xs prev count

binarySearch :: [Int] -> Int -> Int -> Int -> Int -> Int
binarySearch houses c lo hi answer
  | lo > hi = answer
  | canPlace houses c mid = binarySearch houses c (mid + 1) hi mid
  | otherwise = binarySearch houses c lo (mid - 1) answer
  where
    mid = lo + (hi - lo) `div` 2

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Int]
  case values of
    (n:c:rest) -> do
      let houses = sort (take n rest)
          lo = 1
          hi = last houses - head houses
          answer = binarySearch houses c lo hi 0
      print answer
    _ -> return ()