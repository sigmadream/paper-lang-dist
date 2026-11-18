module Main where

import Data.List (intercalate, partition)

main :: IO ()
main = do
    input <- getContents
    let xs = map read (words input) :: [Int]
    case xs of
        [] -> return ()
        (n:rest) ->
            let vals = take n rest
                (zeros, nonZeros) = partition (== 0) vals
                result = nonZeros ++ zeros
            in putStrLn (intercalate " " (map show result))