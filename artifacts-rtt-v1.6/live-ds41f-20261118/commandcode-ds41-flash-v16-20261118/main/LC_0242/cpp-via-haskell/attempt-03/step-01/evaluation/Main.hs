module Main where

import Data.List (sort)

main :: IO ()
main = do
    input <- getContents
    let (s:t:_) = words input
    putStrLn (if sort s == sort t then "1" else "0")