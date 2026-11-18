module Main where

import Data.Array

solve :: Array Int String -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid ! r) !! c
        same = and [ (grid ! i) !! j == first
                   | i <- [r .. r + size - 1]
                   , j <- [c .. c + size - 1] ]
    in if same
       then [first]
       else let half = size `div` 2
            in "("
               ++ solve grid r c half
               ++ solve grid r (c + half) half
               ++ solve grid (r + half) c half
               ++ solve grid (r + half) (c + half) half
               ++ ")"

main :: IO ()
main = do
    input <- getContents
    let ls = lines input
    case ls of
        [] -> return ()
        (nStr : rest) -> do
            let n = read nStr :: Int
                rows = take n rest
                grid = listArray (0, n - 1) rows
            putStrLn (solve grid 0 0 n)