module Main where

main :: IO ()
main = do
    s <- getLine
    let t = reverse s
    putStrLn (if s == t then "1" else "0")