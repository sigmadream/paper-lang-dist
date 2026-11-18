module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  input <- getContents
  let (nLine : rest) = lines input
      n = read nLine :: Int
      xs = take n (map read (words (unwords rest)) :: [Integer])
  case xs of
    [] -> return ()
    (x0:more) -> do
      let (best, _) = foldl' step (x0, x0) more
          step (b, c) x = (max b (max x (c + x)), max x (c + x))
      print best