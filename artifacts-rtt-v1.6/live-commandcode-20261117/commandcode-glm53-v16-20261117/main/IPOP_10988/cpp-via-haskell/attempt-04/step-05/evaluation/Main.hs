module Main (main) where

import Data.List (isSuffixOf)

main :: IO ()
main = do
    s <- getLine
    let t = filter (/= '\r') s
    putStrLn (if t == reverse t then "1" else "0")