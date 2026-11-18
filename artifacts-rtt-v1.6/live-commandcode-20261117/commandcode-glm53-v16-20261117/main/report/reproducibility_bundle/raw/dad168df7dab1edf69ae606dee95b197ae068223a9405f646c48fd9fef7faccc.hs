module Main (main) where

import Data.List (transpose)

solve :: [String] -> String
solve grid
  | all (== c) grid' = [c]
  | otherwise = "(" ++ concatMap solve [topLeft, topRight, bottomLeft, bottomRight] ++ ")"
  where
    grid' = concat grid
    c = head grid'
    half = length (head grid) `div` 2
    rows = map (splitAt half) grid
    topLeft = map fst rows
    topRight = map snd rows
    bottomLeft = map fst (drop half rows)
    bottomRight = map snd (drop half rows)

main :: IO ()
main = do
  contents <- getContents
  let (nLine : rest) = lines contents
      n = read nLine :: Int
      grid = take n rest
  putStrLn (solve grid)