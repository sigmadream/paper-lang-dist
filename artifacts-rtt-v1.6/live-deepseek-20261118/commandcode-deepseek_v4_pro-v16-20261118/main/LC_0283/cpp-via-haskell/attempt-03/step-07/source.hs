module Main where

import Data.List (partition)

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    if null tokens
        then return ()
        else do
            let n = read (head tokens) :: Int
                nums = take n (map read (tail tokens) :: [Int])
                (nonZeros, zeros) = partition (/= 0) nums
                result = nonZeros ++ zeros
            putStrLn (unwords (map show result))