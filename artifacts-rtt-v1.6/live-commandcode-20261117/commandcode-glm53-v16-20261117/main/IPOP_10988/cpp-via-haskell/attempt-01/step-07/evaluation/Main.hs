module Main (main :: IO ()) where

main :: IO ()
main = do
    s <- getLine
    let r = reverse s
    putStrLn (if s == r then "1" else "0")