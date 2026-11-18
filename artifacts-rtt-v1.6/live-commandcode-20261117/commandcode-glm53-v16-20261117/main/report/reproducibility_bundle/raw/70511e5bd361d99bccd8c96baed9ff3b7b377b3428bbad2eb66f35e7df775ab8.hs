module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  contents <- getContents
  let (nStr:rest) = words contents
      n = read nStr :: Int
      xs = take n (map read (concatMap words (lines contents) >>= words) rest) :: [Integer]
  case xs of
    [] -> return ()
    (x0:more) -> do
      let step (cur, best) x = let c = max x (cur + x) in (c, max best c)
          (_, best) = foldl' step (x0, x0) more
      print best