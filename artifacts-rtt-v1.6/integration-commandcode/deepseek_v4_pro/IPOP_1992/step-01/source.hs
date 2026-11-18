module Main where

import Data.List (all)

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size
    | allSame = [first]
    | otherwise = "(" ++ solve grid r c half ++
                          solve grid r (c + half) half ++
                          solve grid (r + half) c half ++
                          solve grid (r + half) (c + half) half ++
                          ")"
  where
    half = size `div` 2
    first = grid !! r !! c
    allSame = all (== first) [grid !! i !! j | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]

main :: IO ()
main = do
    input <- getContents
    let ls = lines input
        n = read (head ls) :: Int
        grid = take n (tail ls)
    putStrLn (solve grid 0 0 n)