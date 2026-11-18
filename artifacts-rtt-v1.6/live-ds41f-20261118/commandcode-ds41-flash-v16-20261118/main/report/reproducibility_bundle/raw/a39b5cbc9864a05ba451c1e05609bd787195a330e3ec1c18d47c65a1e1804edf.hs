module Main where

import Data.List (sort)

canPlace :: [Int] -> Int -> Int -> Bool
canPlace [] _ _ = False
canPlace (_:rest) c dist = go rest (head house) 1
  where
    house = []
    go [] _ count = count >= c
    go (h:hs) lastPos count
      | h - lastPos >= dist =
          if count + 1 >= c
            then True
            else go hs h (count + 1)
      | otherwise = go hs lastPos count

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    (n:c:rest) -> do
      let houses = sort (take n rest)
          lo = 1
          hi = last houses - head houses
          answer = search houses c lo hi 0
      print answer
    _ -> return ()

search :: [Int] -> Int -> Int -> Int -> Int -> Int
search houses c lo hi answer
  | lo > hi = answer
  | otherwise =
      let mid = lo + (hi - lo) `div` 2
      in if canPlace houses c mid
           then search houses c (mid + 1) hi mid
           else search houses c lo (mid - 1) answer