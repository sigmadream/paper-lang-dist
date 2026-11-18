module Main where

import Data.Array

main :: IO ()
main = do
    input <- getContents
    let n = read (head (words input)) :: Int
        counts = array (0, n)
            [(i, if i == 0 then 0 else counts ! (i `div` 2) + i `mod` 2) | i <- [0..n]]
    putStrLn (unwords [show (counts ! i) | i <- [0..n]])