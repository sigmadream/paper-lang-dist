module Main (main) where

import Data.List (isPrefixOf)

main :: IO ()
main = do
    inp <- getContents
    let s = takeWhile (`elem` ['a'..'z']) (dropWhile (`notElem` ['a'..'z']) inp)
    if null s
        then return ()
        else putStrLn (if s == reverse s then "1" else "0")