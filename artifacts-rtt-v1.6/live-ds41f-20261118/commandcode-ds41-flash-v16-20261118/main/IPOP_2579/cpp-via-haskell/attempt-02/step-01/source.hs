module Main where

import Data.Array

solve :: Int -> [Int] -> Int
solve n scores = dp ! n
  where
    score = listArray (1, n) scores :: Array Int Int

    dp = array (0, n) ([(0, 0)] ++ [(i, value i) | i <- [1 .. n]]) :: Array Int Int

    value 1 = score ! 1
    value 2 = score ! 1 + score ! 2
    value i = max (dp ! (i - 2)) (dp ! (i - 3) + score ! (i - 1)) + score ! i

main :: IO ()
main = do
  input <- getContents
  let values = map read (words input) :: [Int]
  case values of
    [] -> return ()
    (n : rest) -> print (solve n (take n rest))