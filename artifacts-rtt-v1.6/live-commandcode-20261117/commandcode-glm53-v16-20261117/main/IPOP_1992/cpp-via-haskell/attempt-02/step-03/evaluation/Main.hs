module Main (main) where

import Data.Char (isDigit)

solve :: [String] -> Int -> Int -> Int -> Int -> String
solve grid r c size
  | same      = [first]
  | otherwise = "(" ++ solve grid r c half
                ++ solve grid r (c + half) half
                ++ solve grid (r + half) c half
                ++ solve grid (r + half) (c + half) half ++ ")"
  where
    first = grid !! r !! c
    cells = [grid !! i !! j | i <- [r .. r + size - 1], j <- [c .. c + size - 1]]
    same = all (== first) cells
    half = size `div` 2

main :: IO ()
main = do
  input <- getContents
  let toks = words input
  case toks of
    [] -> return ()
    (nStr:rest) -> do
      let n = read nStr :: Int
          grid = take n rest
      if n == 0
        then return ()
        else putStrLn (solve grid 0 0 n)