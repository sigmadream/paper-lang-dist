module Main (main) where

import Data.List (isInfixOf)

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    (s:_) -> putStrLn (if s == reverse s then "1" else "0")
    []    -> return ()