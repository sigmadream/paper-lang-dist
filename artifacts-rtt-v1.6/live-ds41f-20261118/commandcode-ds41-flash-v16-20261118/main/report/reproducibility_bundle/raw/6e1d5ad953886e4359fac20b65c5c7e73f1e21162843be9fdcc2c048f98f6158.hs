module Main where

import Data.List (sort)
import Data.Char (isSpace)
import System.IO

stripTrailing :: String -> String
stripTrailing = reverse . dropWhile isSpace . reverse

main :: IO ()
main = do
    input <- getContents
    let ls = lines input
    case ls of
        (s:t:_) -> do
            let s' = sort (stripTrailing s)
                t' = sort (stripTrailing t)
            putStrLn (if s' == t' then "1" else "0")
        [s] -> do
            let s' = sort (stripTrailing s)
            putStrLn "0"
        _ -> return ()