module Main (main) where

import Data.Char (isDigit)
import System.IO

solve :: [String] -> Int -> Int -> Int -> String
solve grid r c size
  | allSame = [first]
  | otherwise = "(" ++ concat [solve grid (r + dr) (c + dc) half | (dr, dc) <- [(0,0),(0,half),(half,0),(half,half)]] ++ ")"
  where
    first = grid !! r !! c
    half = size `div` 2
    block = [grid !! i !! j | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]
    allSame = all (== first) block

main :: IO ()
main = do
    contents <- getContents
    let (nLine : rest) = lines contents
        n = read nLine :: Int
        grid = take n rest
    putStrLn (solve grid 0 0 n)