module Main (main) where

import Data.List (isSuffixOf)

main :: IO ()
main = do
    inp <- getContents
    let ws = words inp
    case ws of
        (s:_) -> putStrLn (if s == reverse s then "1" else "0")
        []    -> return ()