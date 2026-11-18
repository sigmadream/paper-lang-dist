module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  contents <- getContents
  let (nStr : rest) = lines contents
      n = read nStr :: Int
      xs = take n . map read . concatMap words $ rest :: [Integer]
      solve (cur, best) x = (max x (cur + x), max best (max x (cur + x)))
      (_, best) = foldl' solve (head xs, head xs) (tail xs)
  print best