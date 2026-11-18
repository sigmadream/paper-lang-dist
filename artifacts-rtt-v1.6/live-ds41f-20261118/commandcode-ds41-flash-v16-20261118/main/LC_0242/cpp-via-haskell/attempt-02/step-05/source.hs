module Main where

import Data.List (sort)

validAnagram :: String -> String -> Bool
validAnagram s t = length s == length t && sort s == sort t

main :: IO ()
main = do
    input <- getContents
    case words input of
        (s:t:_) -> putStrLn $ if validAnagram s t then "1" else "0"
        _       -> putStrLn "0"