module Main (main) where

main :: IO ()
main = do
    s <- getLine
    putStrLn (if s == reverse s then "1" else "0")