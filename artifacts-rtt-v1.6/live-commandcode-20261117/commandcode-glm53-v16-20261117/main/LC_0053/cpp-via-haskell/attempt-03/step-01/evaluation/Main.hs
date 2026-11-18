module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let (nLine:rest) = lines input
      n = read nLine :: Int
      nums = map read (take n (words (unwords rest))) :: [Int]
  case nums of
    [] -> return ()
    (x:xs) -> do
      let (best, _) = foldl' step (x, x) xs
          step (b, c) v = let c' = max v (c + v) in (max b c', c')
      print best