module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  line <- getLine
  let [m, n] = map read (words line) :: [Int]
      dp0 = replicate n (1 :: Integer)
      step dp = scanl1 (+) dp
      dp = foldl' (const step) dp0 [1 .. m - 1]
  print (last dp)