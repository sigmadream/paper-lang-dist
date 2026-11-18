module Main where

import Data.List (lines)

solve :: [[Char]] -> Int -> Int -> Int -> String
solve grid r c size
  | allSame = [first]
  | otherwise = "(" ++ solve grid r c half
                     ++ solve grid r (c + half) half
                     ++ solve grid (r + half) c half
                     ++ solve grid (r + half) (c + half) half
                     ++ ")"
  where
    half = size `div` 2
    first = (grid !! r) !! c
    allSame = all (\i -> all (\j -> (grid !! (r + i)) !! (c + j) == first) [0..size-1]) [0..size-1]

main :: IO ()
main = do
  input <- getContents
  let ls = lines input
  case ls of
    (nStr:rest) -> do
      let n = read nStr :: Int
      let grid = take n rest
      putStrLn (solve grid 0 0 n)
    _ -> return ()