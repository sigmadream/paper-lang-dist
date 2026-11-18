module Main where

import Data.List (sort, foldl')

countPlacements :: Int -> [Int] -> Int
countPlacements d (x:xs) = fst $ foldl' step (1, x) xs
  where
    step (cnt, prev) y
      | y - prev >= d = (cnt + 1, y)
      | otherwise     = (cnt, prev)
countPlacements _ [] = 0

solve :: Int -> [Int] -> Int
solve c xs = search left right 0
  where
    left = 1
    right = last xs - head xs

    search lo hi ans
      | lo > hi = ans
      | otherwise =
          let mid = lo + (hi - lo) `div` 2
              cnt = countPlacements mid xs
          in if cnt >= c
               then search (mid + 1) hi mid
               else search lo (mid - 1) ans

main :: IO ()
main = do
    input <- getContents
    let (n:c:rest) = map read (words input) :: [Int]
        homes = sort (take n rest)
    print (solve c homes)