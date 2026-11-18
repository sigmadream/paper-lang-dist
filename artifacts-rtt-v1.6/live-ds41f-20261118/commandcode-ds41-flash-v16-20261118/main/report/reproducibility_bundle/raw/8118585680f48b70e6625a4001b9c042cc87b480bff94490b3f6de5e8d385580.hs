module Main where

import Data.List (sort)

canPlace :: [Int] -> Int -> Int -> Bool
canPlace [] _ _ = False
canPlace (firstHouse:rest) c d = go 1 firstHouse rest
  where
    go count _ [] = count >= c
    go count prev (x:xs)
      | x - prev >= d = go (count + 1) x xs
      | otherwise = go count prev xs

binarySearch :: [Int] -> Int -> Int -> Int -> Int -> Int
binarySearch houses c lo hi ans
  | lo > hi = ans
  | otherwise =
      let mid = lo + (hi - lo) `div` 2
      in if canPlace houses c mid
           then binarySearch houses c (mid + 1) hi mid
           else binarySearch houses c lo (mid - 1) ans

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    (nStr:cStr:rest) -> do
      let n = read nStr :: Int
          c = read cStr :: Int
          houses = sort (map read (take n rest) :: [Int])
          answer = binarySearch houses c 1 (last houses - head houses) 0
      print answer
    _ -> return ()