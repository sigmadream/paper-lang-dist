module Main where

import Data.List (lines)

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = grid !! r !! c
        allSame = all (== first) [grid !! i !! j | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]
    in if allSame
         then [first]
         else let half = size `div` 2
              in  "(" ++ solve grid r c half
                        ++ solve grid r (c + half) half
                        ++ solve grid (r + half) c half
                        ++ solve grid (r + half) (c + half) half
                        ++ ")"

main :: IO ()
main = do
    content <- getContents
    let allLines = lines content
        n = read (head allLines) :: Int
        grid = take n (tail allLines)
    putStrLn (solve grid 0 0 n)