module Main (main) where

import Data.List (isPrefixOf)

main :: IO ()
main = do
  s <- getLine
  let t = takeWhile (\c -> c >= 'a' && c <= 'z') s
  putStrLn (if t == reverse t then "1" else "0")