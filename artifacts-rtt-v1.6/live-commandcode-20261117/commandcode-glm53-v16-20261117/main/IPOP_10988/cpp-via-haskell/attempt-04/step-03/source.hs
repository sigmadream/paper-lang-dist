module Main (main) where

import Data.List (isSuffixOf)

main :: IO ()
main = do
    ms <- fmap (fmap (filter (/= '\n')) . Just) getLine
    case ms of
        Nothing -> return ()
        Just s  -> putStrLn (if s == reverse s then "1" else "0")