module Main (main) where

import Data.List (isPrefixOf)

main :: IO ()
main = do
    contents <- getContents
    let ws = words contents
    case ws of
        (s:_) -> putStrLn (if s == reverse s then "1" else "0")
        []    -> return ()