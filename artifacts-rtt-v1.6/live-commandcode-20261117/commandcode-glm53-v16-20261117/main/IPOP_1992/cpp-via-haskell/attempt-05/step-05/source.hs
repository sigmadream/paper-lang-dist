module Main (main) where

import Data.Array (Array, listArray, (!), bounds)

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size
  | same      = [first]
  | otherwise = "(" ++ concat [ solve grid (r + dr) (c + dc) half | (dr, dc) <- quads ] ++ ")"
  where
    first = grid ! (r, c)
    half = size `div` 2
    same = all (\(i, j) -> grid ! (i, j) == first) cells
    cells = [ (i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1] ]
    quads = [(0, 0), (0, half), (half, 0), (half, half)]

main :: IO ()
main = do
  contents <- getContents
  let (nLine : rest) = lines contents
      n = read nLine :: Int
      grid = listArray ((0, 0), (n - 1, n - 1)) (concat (take n rest))
  putStrLn (solve grid 0 0 n)