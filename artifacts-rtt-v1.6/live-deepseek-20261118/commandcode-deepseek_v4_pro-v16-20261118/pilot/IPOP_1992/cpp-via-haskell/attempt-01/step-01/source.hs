module Main where

import System.IO

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size
    | allSame   = [first]
    | otherwise = "(" ++ tl ++ tr ++ bl ++ br ++ ")"
  where
    first = (grid !! r) !! c
    allSame = all (\i -> all (\j -> (grid !! (r + i)) !! (c + j) == first) [0 .. size - 1]) [0 .. size - 1]
    half = size `div` 2
    tl = solve grid r c half
    tr = solve grid r (c + half) half
    bl = solve grid (r + half) c half
    br = solve grid (r + half) (c + half) half

main :: IO ()
main = do
    input <- getContents
    let ls = lines input
    case ls of
        (nStr : rest) -> do
            let n = read nStr :: Int
                grid = take n rest
            putStrLn (solve grid 0 0 n)
        _ -> return ()