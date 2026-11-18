module Main where

import Data.List (sort)

countPlacements :: Int -> [Int] -> Int
countPlacements d (x:xs) = go 1 x xs
  where
    go count _ [] = count
    go count prev (y:ys)
      | y - prev >= d = go (count + 1) y ys
      | otherwise     = go count prev ys
countPlacements _ [] = 0

binarySearch :: [Int] -> Int -> Int -> Int -> Int -> Int
binarySearch homes c left right answer
  | left > right = answer
  | otherwise =
      let mid = left + (right - left) `div` 2
      in if countPlacements mid homes >= c
           then binarySearch homes c (mid + 1) right mid
           else binarySearch homes c left (mid - 1) answer

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Int]
  case values of
    (n:c:rest) ->
      let homes = sort (take n rest)
          left = 1
          right = last homes - head homes
      in print (binarySearch homes c left right 0)
    _ -> return ()