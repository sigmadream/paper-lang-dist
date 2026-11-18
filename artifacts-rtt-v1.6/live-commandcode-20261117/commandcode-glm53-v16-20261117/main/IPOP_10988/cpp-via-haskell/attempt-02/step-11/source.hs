module Main (main) where

import Data.Char (isLower)

main :: IO ()
main = do
  line <- getLine
  let t = takeWhile isLower line
      r = reverse t
  putStrLn (if t == r then "1" else "0")