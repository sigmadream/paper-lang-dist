module Main (main) where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size
  | same = [first]
  | otherwise = "(" ++ concat (map quad [0,1,2,3]) ++ ")"
  where
    first = grid ! (r, c)
    half = size `div` 2
    same = all (\(i, j) -> grid ! (i, j) == first)
           [(i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]
    quad q =
      let (dr, dc) = [(0, 0), (0, 1), (1, 0), (1, 1)] !! q
      in solve grid (r + dr * half) (c + dc * half) half

main :: IO ()
main = do
  contents <- getContents
  let (nLine : rest) = lines contents
      n = read nLine :: Int
      gridRows = take n rest
      grid = listArray ((0, 0), (n - 1, n - 1))
             [ gridRows !! i !! j | i <- [0 .. n - 1], j <- [0 .. n - 1] ] :: Array (Int, Int) Char
  putStrLn (solve grid 0 0 n)