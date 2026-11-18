module Main (main) where

import Data.Char (isLower)

main :: IO ()
main = do
  s <- getLine
  let t = takeWhile isLower s
      r = reverse t
  putStrLn (if t == r then "1" else "0")