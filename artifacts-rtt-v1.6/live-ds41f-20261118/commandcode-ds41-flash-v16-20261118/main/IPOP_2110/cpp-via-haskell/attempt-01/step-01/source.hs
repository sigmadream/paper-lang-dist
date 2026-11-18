module Main where

import Data.List (sort)

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        (nStr : cStr : rest) -> do
            let n = read nStr :: Int
                c = read cStr :: Int
                houses = sort (map read (take n rest) :: [Int])
            if null houses
                then return ()
                else do
                    let left = 1
                        right = last houses - head houses
                        answer = binarySearch houses c left right 0
                    print answer
        _ -> return ()

binarySearch :: [Int] -> Int -> Int -> Int -> Int -> Int
binarySearch houses c left right answer
    | left > right = answer
    | otherwise =
        let mid = left + (right - left) `div` 2
            count = countInstall houses mid
        in if count >= c
               then binarySearch houses c (mid + 1) right mid
               else binarySearch houses c left (mid - 1) answer

countInstall :: [Int] -> Int -> Int
countInstall [] _ = 0
countInstall (x : xs) distance = go xs x 1
  where
    go [] _ count = count
    go (y : ys) prev count
        | y - prev >= distance = go ys y (count + 1)
        | otherwise = go ys prev count