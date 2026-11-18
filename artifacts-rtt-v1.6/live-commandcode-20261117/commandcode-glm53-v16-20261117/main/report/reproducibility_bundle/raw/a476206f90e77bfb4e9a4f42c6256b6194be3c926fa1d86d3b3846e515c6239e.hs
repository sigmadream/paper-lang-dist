module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  let (nLine : rest) = lines inp
      n = read nLine :: Int
      xs = take n (map read (words (unlines rest))) :: [Int]
  case xs of
    [] -> return ()
    (x0:more) -> do
      let step (cur, best) x = (max x (cur + x), max best (max x (cur + x)))
          (_, best) = foldl' step (x0, x0) more
      print best