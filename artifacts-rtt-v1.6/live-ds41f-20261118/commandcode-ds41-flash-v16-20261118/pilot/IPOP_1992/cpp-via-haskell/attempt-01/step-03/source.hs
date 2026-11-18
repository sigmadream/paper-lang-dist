module Main where

import Data.Array

sameRegion :: Array (Int, Int) Char -> Int -> Int -> Int -> Bool
sameRegion grid r c size =
  let first = grid ! (r, c)
  in all (\i -> all (\j -> grid ! (i, j) == first) [c .. c + size - 1])
         [r .. r + size - 1]

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve grid r c size
  | sameRegion grid r c size = [grid ! (r, c)]
  | otherwise =
      "("
      ++ solve grid r c half
      ++ solve grid r (c + half) half
      ++ solve grid (r + half) c half
      ++ solve grid (r + half) (c + half) half
      ++ ")"
  where
    half = size `div` 2

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (ns:rows) -> do
      let n = read ns :: Int
          grid = listArray ((0, 0), (n - 1, n - 1)) (concat (take n rows))
      putStrLn (solve grid 0 0 n)