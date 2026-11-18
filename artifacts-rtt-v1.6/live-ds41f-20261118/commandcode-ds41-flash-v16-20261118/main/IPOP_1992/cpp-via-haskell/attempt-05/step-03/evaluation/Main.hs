module Main where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size =
    let first = grid ! (r, c)
        allSame = all (\(i, j) -> grid ! (i, j) == first)
                      [(i, j) | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]
    in if allSame
       then [first]
       else let half = size `div` 2
                tl = solve grid r c half
                tr = solve grid r (c + half) half
                bl = solve grid (r + half) c half
                br = solve grid (r + half) (c + half) half
            in "(" ++ tl ++ tr ++ bl ++ br ++ ")"

main :: IO ()
main = do
    contents <- getContents
    let tokens = words contents
    case tokens of
        [] -> return ()
        (nStr : rest) -> do
            let n = read nStr :: Int
                rows = take n rest
                grid = listArray ((0, 0), (n - 1, n - 1))
                                 [rows !! i !! j | i <- [0 .. n - 1], j <- [0 .. n - 1]]
            putStrLn (solve grid 0 0 n)