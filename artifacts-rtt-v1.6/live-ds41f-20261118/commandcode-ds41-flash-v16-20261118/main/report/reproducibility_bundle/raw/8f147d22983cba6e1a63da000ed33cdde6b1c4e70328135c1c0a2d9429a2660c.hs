module Main where

import Data.Array

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        [] -> return ()
        (x:xs) -> do
            let n = read x :: Int
                scores = take n (map read xs)
                arr = listArray (1, n) scores :: Array Int Int
                dpArr = listArray (0, n) [dpval i | i <- [0..n]] :: Array Int Int
                dpval 0 = 0
                dpval 1 = arr ! 1
                dpval 2 = arr ! 1 + arr ! 2
                dpval i = max (dpArr ! (i - 2)) (dpArr ! (i - 3) + arr ! (i - 1)) + arr ! i
            putStrLn (show (dpArr ! n))