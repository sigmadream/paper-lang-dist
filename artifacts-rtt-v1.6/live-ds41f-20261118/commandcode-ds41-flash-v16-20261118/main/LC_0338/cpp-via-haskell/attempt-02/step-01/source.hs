module Main where

import Data.Array
import Data.List (words)

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    let n = if null tokens then 0 else read (head tokens) :: Int
    let counts = listArray (0, n) [if i == 0 then 0 else counts ! (i `div` 2) + i `mod` 2 | i <- [0..n]]
    putStrLn $ unwords $ map show $ elems counts