module Main (main) where

import Data.List (isSuffixOf)

main :: IO ()
main = do
  s <- getLine
  let t = filter (/= '\r') s
      r = reverse t
  putStrLn (if t == r then "1" else "0")