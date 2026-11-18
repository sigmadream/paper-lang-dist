module Main where

import Data.List (intercalate)

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        (nStr : rest) -> do
            let n = read nStr :: Int
            let nums = take n (map read rest :: [Int])
            let nonZeros = filter (/= 0) nums
            let zeroCount = length nums - length nonZeros
            let result = nonZeros ++ replicate zeroCount 0
            putStrLn $ intercalate " " (map show result)
        [] -> return ()