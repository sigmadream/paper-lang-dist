module Main (main) where

import Data.Array

main :: IO ()
main = do
  contents <- getContents
  let (n : rest) = map read (words contents) :: [Int]
      scores = listArray (1, n) rest :: Array Int Int
      dp :: Array Int Int
      dp = listArray (1, n) [f i | i <- [1 .. n]]
      f 1 = scores ! 1
      f 2 = scores ! 1 + scores ! 2
      f i = max (dp ! (i - 2)) (dp ! (i - 3) + scores ! (i - 1)) + scores ! i
  print (dp ! n)