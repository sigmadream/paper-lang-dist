module Main (main) where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size
  | allSame = [first]
  | otherwise = "(" ++ concatMap quad [(r, c), (r, c + half), (r + half, c), (r + half, c + half)] ++ ")"
  where
    first = grid ! (r, c)
    half = size `div` 2
    allSame = all (\(i, j) -> grid ! (i, j) == first)
                  [(i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]
    quad (rr, cc) = solve grid rr cc half
    -- half defined above; quad uses it directly

main :: IO ()
main = do
  contents <- getContents
  let (nLine : rest) = lines contents
      n = read nLine :: Int
      rows = take n rest
      grid = listArray ((0, 0), (n - 1, n - 1))
             [ rows !! i !! j | i <- [0 .. n - 1], j <- [0 .. n - 1] ]
  putStrLn (solve grid 0 0 n)