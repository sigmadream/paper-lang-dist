module Main where

import Data.List (partition)

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
        n = read (head tokens) :: Int
        nums = map read (take n (tail tokens)) :: [Int]
        (nonZeros, zeros) = partition (/= 0) nums
    putStrLn $ unwords $ map show (nonZeros ++ zeros)