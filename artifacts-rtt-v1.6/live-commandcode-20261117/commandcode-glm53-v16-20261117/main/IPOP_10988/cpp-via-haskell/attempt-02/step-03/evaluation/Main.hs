module Main (main) where

import Data.List (isSuffixOf)

main :: IO ()
main = do
    s <- getLine
    let t = takeWhile (>= 'a') . takeWhile (<= 'z') $ s
        r = reverse t
    putStrLn (if t == r then "1" else "0")