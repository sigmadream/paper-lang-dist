module Main where

import Data.Array (Array, listArray, (!))

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (x:_) -> do
            let n = read x :: Int
                counts = listArray (0, n) [count i | i <- [0..n]] :: Array Int Int
                count 0 = 0
                count i = counts ! (i `div` 2) + (i `mod` 2)
            putStrLn $ unwords $ map (show . (counts !)) [0..n]