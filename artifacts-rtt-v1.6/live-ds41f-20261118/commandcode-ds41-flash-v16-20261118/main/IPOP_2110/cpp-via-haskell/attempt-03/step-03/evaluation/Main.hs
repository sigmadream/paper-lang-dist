module Main where

import Data.List (sort)

canPlace :: Int -> [Int] -> Int -> Bool
canPlace c houses dist = go (tail houses) 1 (head houses)
  where
    go [] count _ = count >= c
    go (h:hs) count lastPos
      | h - lastPos >= dist =
          if count + 1 >= c
            then True
            else go hs (count + 1) h
      | otherwise = go hs count lastPos

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    (n:c:rest) -> do
      let houses = sort (take n rest)
          lo = 1
          hi = last houses - head houses
          answer = binarySearch houses c lo hi 0
      print answer
    _ -> return ()

binarySearch :: [Int] -> Int -> Int -> Int -> Int -> Int
binarySearch houses c lo hi answer
  | lo > hi = answer
  | otherwise =
      let mid = lo + (hi - lo) `div` 2
      in if canPlace c houses mid
           then binarySearch houses c (mid + 1) hi mid
           else binarySearch houses c lo (mid - 1) answer