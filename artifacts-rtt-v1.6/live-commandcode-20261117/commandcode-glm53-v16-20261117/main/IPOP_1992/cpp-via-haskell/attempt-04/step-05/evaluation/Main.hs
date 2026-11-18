module Main (main) where

import Data.List (intercalate)

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        same = all (\i -> all (\j -> (grid !! i) !! j == first) [c .. c + size - 1]) [r .. r + size - 1]
    in if same
        then [first]
        else
            let half = size `div` 2
                quads = [ (dr, dc) | dr <- [0, half], dc <- [0, half] ]
                -- order: top-left, top-right, bottom-left, bottom-right
                order = [ (0, 0), (0, half), (half, 0), (half, half) ]
            in "(" ++ concatMap (\(dr, dc) -> solve grid (r + dr) (c + dc) half) order ++ ")"

main :: IO ()
main = do
    contents <- getContents
    let ls = lines contents
        n = read (head ls) :: Int
        grid = take n (tail ls)
    putStrLn (solve grid 0 0 n)