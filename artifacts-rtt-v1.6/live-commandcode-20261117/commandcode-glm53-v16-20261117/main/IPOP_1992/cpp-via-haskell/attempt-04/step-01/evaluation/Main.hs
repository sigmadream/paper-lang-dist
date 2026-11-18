module Main (main) where

import System.IO

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = grid !! r !! c
        region = take size (drop r grid)
        same = all (\row -> all (== first) (take size (drop c row))) region
    in if same then [first]
       else let half = size `div` 2
                tl = solve grid r c half
                tr = solve grid r (c + half) half
                bl = solve grid (r + half) c half
                br = solve grid (r + half) (c + half) half
            in "(" ++ tl ++ tr ++ bl ++ br ++ ")"

main :: IO ()
main = do
    hSetEncoding stdin utf8
    contents <- getContents
    let (nLine : rest) = lines contents
        n = read nLine :: Int
        grid = take n rest
    putStrLn (solve grid 0 0 n)