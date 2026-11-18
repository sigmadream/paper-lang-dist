module Main (main) where

import Data.List (isInfixOf)

main :: IO ()
main = do
    m <- getLine
    let s = takeWhile (`elem` ['a'..'z']) m
    if not (null s)
        then putStrLn (if s == reverse s then "1" else "0")
        else return ()