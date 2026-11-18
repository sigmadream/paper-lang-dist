module Main where

import Data.Array

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size
    | allSame = [first]
    | otherwise = "("
        ++ solve grid r c half
        ++ solve grid r (c + half) half
        ++ solve grid (r + half) c half
        ++ solve grid (r + half) (c + half) half
        ++ ")"
  where
    first = grid ! (r, c)
    half = size `div` 2
    allSame = and [grid ! (i, j) == first
                  | i <- [r .. r + size - 1]
                  , j <- [c .. c + size - 1]]

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (nStr : rest) -> do
            let n = read nStr :: Int
                rows = take n rest
                grid = listArray ((0, 0), (n - 1, n - 1)) (concat rows)
            putStrLn (solve grid 0 0 n)