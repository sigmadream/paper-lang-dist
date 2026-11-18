module Main where

main :: IO ()
main = do
    input <- getContents
    let s = head (words input)
        t = reverse s
    putStrLn (if s == t then "1" else "0")