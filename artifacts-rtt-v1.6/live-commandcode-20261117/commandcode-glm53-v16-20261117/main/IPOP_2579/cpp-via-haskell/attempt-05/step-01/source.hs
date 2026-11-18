module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  contents <- getContents
  let (nStr:rest) = lines contents
      n = read nStr :: Int
      scores = map read (take n rest) :: [Int]
      s = 0 : scores -- 1-indexed
      answer
        | n == 0 = 0
        | n == 1 = s !! 1
        | otherwise =
            let dp1 = s !! 1
                dp2 = (s !! 1) + (s !! 2)
                go (d1, d2, d3) i = (d2, max d1 (d3 + s !! (i - 1)) + s !! i, d2)
                (finalD2, _, _) = foldl' go (dp1, dp2, 0) [3 .. n]
            in finalD2
  print answer