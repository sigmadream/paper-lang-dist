module Main where

import Data.List (sort)

countPlacements :: Int -> [Int] -> Int
countPlacements d homes = go 1 (head homes) (tail homes)
  where
    go cnt _ [] = cnt
    go cnt prev (x:xs)
      | x - prev >= d = go (cnt + 1) x xs
      | otherwise     = go cnt prev xs

main :: IO ()
main = do
  input <- getContents
  let (n:c:rest) = map read (words input) :: [Int]
      homes = sort (take n rest)

      search :: Int -> Int -> Int -> Int
      search left right best
        | left > right = best
        | otherwise =
            let mid = left + (right - left) `div` 2
            in if countPlacements mid homes >= c
                 then search (mid + 1) right mid
                 else search left (mid - 1) best

      left = 1
      right = last homes - head homes
      ans = search left right 0

  print ans