module Main where

import Data.List (sort)

isCWhitespace :: Char -> Bool
isCWhitespace c = c == ' ' || c == '\t' || c == '\n' ||
                  c == '\v' || c == '\f' || c == '\r'

stripTrailing :: String -> String
stripTrailing = reverse . dropWhile isCWhitespace . reverse

main :: IO ()
main = do
    input <- getContents
    case lines input of
        [] -> return ()
        [_] -> putStr "0\n"
        (l1 : l2 : _) -> do
            let s = sort (stripTrailing l1)
                t = sort (stripTrailing l2)
            putStr (if s == t then "1\n" else "0\n")