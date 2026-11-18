module Main where

import Data.List (partition)

main :: IO ()
main = do
    input <- getContents
    let nums = map read (words input) :: [Int]
    case nums of
        [] -> return ()
        (n:rest) ->
            let arr = take n rest
                (zeros, nonZeros) = partition (== 0) arr
            in putStrLn (unwords (map show (nonZeros ++ zeros)))