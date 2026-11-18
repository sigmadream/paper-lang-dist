module Main (main) where

import Data.List (isSuffixOf)

main :: IO ()
main = do
  m <- getLine
  let s = takeWhile (\c -> c >= 'a' && c <= 'z') m
  if not (null s)
    then putStrLn (if s == reverse s then "1" else "0")
    else return ()