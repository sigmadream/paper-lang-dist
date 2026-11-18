module Main where

import Data.List (sort)

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    case ws of
        (s:t:_) -> putStrLn (if sort s == sort t then "1" else "0")
        _       -> putStrLn "0"