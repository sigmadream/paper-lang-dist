module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  contents <- getContents
  case words contents of
    (nStr:rest) | (read nStr :: Int) > 0, not (null rest) -> do
      let a = map read (take [] rest) :: [Integer]
          go (cur, best) x = (max x (cur + x), max best (max x (cur + x)))
          (_, best) = foldl' go (head a, head a) (tail a)
      putStrLn (show best)
    _ -> return ()