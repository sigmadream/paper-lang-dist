module Main where

main :: IO ()
main = do
    input <- getLine
    let s = takeWhile (/= ' ') input
    putStrLn (if s == reverse s then "1" else "0")