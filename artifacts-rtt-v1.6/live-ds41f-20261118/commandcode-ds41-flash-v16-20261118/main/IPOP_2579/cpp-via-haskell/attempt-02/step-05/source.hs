module Main where

import Data.Array

main :: IO ()
main = do
  contents <- getContents
  let vals = map read (words contents) :: [Int]
  case vals of
    [] -> return ()
    (n:rest) -> do
      let scores = take n rest
          ans = solve n scores
      print ans

solve :: Int -> [Int] -> Int
solve 0 _ = 0
solve n scores =
  let s = listArray (1, n) scores :: Array Int Int
      dp = listArray (0, n) ([0] ++ [value i | i <- [1..n]]) :: Array Int Int
      value 1 = s ! 1
      value 2 = s ! 1 + s ! 2
      value i = max (dp ! (i - 2)) (dp ! (i - 3) + s ! (i - 1)) + s ! i
  in dp ! n