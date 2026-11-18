module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  let (nStr:rest) = words inp
      n = read nStr :: Int
      xs = take n (map read rest) :: [Integer]
      go (best, cur) x = let c = max x (cur + x) in (max best c, c)
      (best, _) = foldl' go (head xs, head xs) (tail xs)
  print best