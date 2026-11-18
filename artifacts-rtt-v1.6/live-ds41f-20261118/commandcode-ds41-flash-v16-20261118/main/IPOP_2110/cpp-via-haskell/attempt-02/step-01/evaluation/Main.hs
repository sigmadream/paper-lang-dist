module Main where

import Data.List (sort)

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        (nStr : cStr : rest) -> do
            let n = read nStr :: Int
                c = read cStr :: Int
                houses = sort (take n (map read rest :: [Int]))
                left = 1
                right = last houses - head houses
                answer = binarySearch houses c left right 0
            print answer
        _ -> return ()

binarySearch :: [Int] -> Int -> Int -> Int -> Int -> Int
binarySearch houses c left right answer
    | left > right = answer
    | otherwise =
        let mid = left + (right - left) `div` 2
            installed = countInstalled houses mid
        in if installed >= c
               then binarySearch houses c (mid + 1) right mid
               else binarySearch houses c left (mid - 1) answer

countInstalled :: [Int] -> Int -> Int
countInstalled [] _ = 0
countInstalled (firstHouse : rest) distance = go rest firstHouse 1
  where
    go [] _ count = count
    go (house : houses) previous count
        | house - previous >= distance = go houses house (count + 1)
        | otherwise = go houses previous count