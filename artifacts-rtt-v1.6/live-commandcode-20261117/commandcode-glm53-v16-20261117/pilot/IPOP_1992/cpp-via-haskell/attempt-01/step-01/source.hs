module Main (main) where

import Data.Array
import System.IO

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size =
    let first = grid ! (r, c)
        cells = [ grid ! (i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1] ]
    in if all (== first) cells
         then [first]
         else
            let half = size `div` 2
                tl = solve grid r c half
                tr = solve grid r (c + half) half
                bl = solve grid (r + half) c half
                br = solve grid (r + half) (c + half) half
            in "(" ++ tl ++ tr ++ bl ++ br ++ ")"

main :: IO ()
main = do
    contents <- getContents
    let (nLine : rest) = lines contents
        n = read nLine :: Int
        grid = listArray ((0, 0), (n - 1, n - 1)) (concat rest)
    putStrLn (solve grid 0 0 n)