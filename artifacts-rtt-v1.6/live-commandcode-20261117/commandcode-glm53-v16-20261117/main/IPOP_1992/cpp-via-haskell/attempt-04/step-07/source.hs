module Main (main) where

import System.IO

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size
  | allSame   = [first]
  | otherwise = "(" ++ concat [solve grid (r + dr) (c + dc) half | (dr, dc) <- offsets] ++ ")"
  where
    first = grid !! r !! c
    allSame = and [ grid !! i !! j == first | i <- [r .. r + size - 1], j <- [c .. c + size - 1] ]
    half = size `div` 2
    offsets = [(0, 0), (0, half), (half, 0), (half, half)]

main :: IO ()
main = do
  contents <- getContents
  let (nLine : rest) = lines contents
      n = read nLine :: Int
      grid = take n rest
  putStrLn (solve grid 0 0 n)