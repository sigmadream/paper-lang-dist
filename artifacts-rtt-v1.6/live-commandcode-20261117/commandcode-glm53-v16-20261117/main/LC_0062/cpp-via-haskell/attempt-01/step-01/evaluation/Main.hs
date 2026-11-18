module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  line <- getLine
  let [m, n] = map read (words line) :: [Int]
  let dp = foldl' step (replicate n 1) [1 .. m - 1]
      step row _ = scanl1 (+) row
  print (last dp)