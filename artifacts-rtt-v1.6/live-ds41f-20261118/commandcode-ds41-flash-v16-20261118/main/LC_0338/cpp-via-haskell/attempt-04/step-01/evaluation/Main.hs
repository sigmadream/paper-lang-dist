module Main where

import Data.Array (Array, listArray, (!))
import Data.List (intercalate)

main :: IO ()
main = do
    input <- getContents
    let n = read (head (words input)) :: Int
        counts :: Array Int Int
        counts = listArray (0, n)
            [ if i == 0 then 0 else counts ! (i `div` 2) + (i `mod` 2)
            | i <- [0..n]
            ]
        result = intercalate " " (map (show . (counts !)) [0..n])
    putStrLn result