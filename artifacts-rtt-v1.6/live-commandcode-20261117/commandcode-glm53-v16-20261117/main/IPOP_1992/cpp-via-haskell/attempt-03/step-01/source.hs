module Main (main) where

import Data.List (isPrefixOf)

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        region = [[(grid !! (r+i)) !! (c+j) | j <- [0..size-1]] | i <- [0..size-1]]
    in if all (all (== first)) region
       then [first]
       else let half = size `div` 2
                tl = solve grid r c half
                tr = solve grid r (c+half) half
                bl = solve grid (r+half) c half
                br = solve grid (r+half) (c+half) half
            in "(" ++ tl ++ tr ++ bl ++ br ++ ")"

main :: IO ()
main = do
    input <- getContents
    let (nLine : rest) = lines input
        n = read nLine :: Int
        grid = take n rest
    if null grid
       then return ()
       else putStrLn (solve grid 0 0 n)