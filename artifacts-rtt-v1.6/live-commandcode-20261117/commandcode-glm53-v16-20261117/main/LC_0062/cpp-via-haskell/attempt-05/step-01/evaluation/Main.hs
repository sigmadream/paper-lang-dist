module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  line <- getLine
  let [m, n] = map read (words line) :: [Int]
      row = replicate n 1
      step dp = scanl1 (+) dp
      dp = foldl' (\acc _ -> step acc) row [1 .. m - 1]
  print (last dp)