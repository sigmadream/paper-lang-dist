module Main (main) where

import Data.Array

same :: Array (Int, Int) Char -> Int -> Int -> Int -> Bool
same g r c s =
  let ch = g ! (r, c)
  in all (\(i, j) -> g ! (r + i, c + j) == ch) [(i, j) | i <- [0 .. s - 1], j <- [0 .. s - 1]]

solve :: Array (Int, Int) Char -> Int -> Int -> Int -> String
solve g r c s
  | same g r c s = [g ! (r, c)]
  | otherwise =
      let h = s `div` 2
      in "(" ++ solve g r c h ++ solve g r (c + h) h ++ solve g (r + h) c h ++ solve g (r + h) (c + h) h ++ ")"

main :: IO ()
main = do
  contents <- getContents
  let (nStr : rest) = lines contents
      n = read nStr :: Int
      rows = take n rest
      g = listArray ((0, 0), (n - 1, n - 1)) (concat rows) :: Array (Int, Int) Char
  if n > 0
    then putStrLn (solve g 0 0 n)
    else return ()