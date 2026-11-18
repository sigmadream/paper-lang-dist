module Main where

import Control.Monad (replicateM)

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size =
    let first = (grid !! r) !! c
        same = and [ (grid !! i) !! j == first | i <- [r .. r + size - 1], j <- [c .. c + size - 1] ]
    in if same
       then [first]
       else let half = size `div` 2
            in "(" ++ solve grid r c half
                    ++ solve grid r (c + half) half
                    ++ solve grid (r + half) c half
                    ++ solve grid (r + half) (c + half) half
                    ++ ")"

main :: IO ()
main = do
    nLine <- getLine
    let n = read nLine :: Int
    grid <- replicateM n getLine
    putStrLn (solve grid 0 0 n)