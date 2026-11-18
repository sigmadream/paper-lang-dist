module Main (main) where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size =
    let first = grid ! (r, c)
        same = all (\(i, j) -> grid ! (i, j) == first)
                   [(i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]
    in if same then [first]
       else let half = size `div` 2
                tl = solve grid r c half
                tr = solve grid r (c + half) half
                bl = solve grid (r + half) c half
                br = solve grid (r + half) (c + half) half
            in "(" ++ tl ++ tr ++ bl ++ br' ++ ")"
  where
    br' = solve grid (r + size `div` 2) (c + size `div` 2) (size `div` 2)

main :: IO ()
main = do
    input <- getContents
    let (nLine : rest) = lines input
        n = read nLine :: Int
        gridRows = take n rest
        grid = listArray ((0, 0), (n - 1, n - 1))
               [ (gridRows !! i) !! j | i <- [0 .. n - 1], j <- [0 .. n - 1] ]
    if n == 0 then return () else putStrLn (solve grid 0 0 n)