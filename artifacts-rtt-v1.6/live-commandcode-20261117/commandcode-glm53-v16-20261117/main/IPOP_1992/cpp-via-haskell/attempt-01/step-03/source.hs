module Main (main) where

import Data.Array
import System.IO

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size
    | same      = [first]
    | otherwise = "(" ++ solve grid r c half ++ solve grid r (c + half) half
                      ++ solve grid (r + half) c half ++ solve grid (r + half) (c + half) half ++ ")"
  where
    first = grid ! (r, c)
    half = size `div` 2
    cells = [ grid ! (i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1] ]
    same = all (== first) cells

main :: IO ()
main = do
    contents <- getContents
    let (nLine : rest) = lines contents
        n = read nLine :: Int
        rows = take n rest
        grid = listArray ((0, 0), (n - 1, n - 1)) (concat rows)
    putStrLn (solve grid 0 0 n)