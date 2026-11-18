module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  contents <- getContents
  let (nStr : rest) = contentsLine
      n = read nStr :: Int
      scores = map read (take n rest) :: [Int]
      s = 0 : scores -- 1-indexed
      dp = scanl step 0 [1 .. n]
      step _ i
        | i == 1 = s !! 1
        | i == 2 = s !! 1 + s !! 2
        | otherwise = max (dp !! (i - 2)) (dp !! (i - 3) + s !! (i - 1)) + s !! i
  print (last dp)