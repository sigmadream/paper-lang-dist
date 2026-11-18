module Main where

import Data.List (sort)

canPlace :: [Int] -> Int -> Int -> Bool
canPlace [] _ _ = False
canPlace (first:rest) c d = go 1 first rest
  where
    go count _ [] = count >= c
    go count prev (x:xs)
      | x - prev >= d = go (count + 1) x xs
      | otherwise = go count prev xs

search :: [Int] -> Int -> Int -> Int -> Int -> Int
search houses c lo hi ans
  | lo > hi = ans
  | canPlace houses c mid = search houses c (mid + 1) hi mid
  | otherwise = search houses c lo (mid - 1) ans
  where
    mid = lo + (hi - lo) `div` 2

main :: IO ()
main = do
  contents <- getContents
  let nums = map read (words contents) :: [Int]
  case nums of
    (n:c:rest) -> do
      let houses = sort (take n rest)
          hi = last houses - head houses
      print (search houses c 1 hi 0)
    _ -> return ()