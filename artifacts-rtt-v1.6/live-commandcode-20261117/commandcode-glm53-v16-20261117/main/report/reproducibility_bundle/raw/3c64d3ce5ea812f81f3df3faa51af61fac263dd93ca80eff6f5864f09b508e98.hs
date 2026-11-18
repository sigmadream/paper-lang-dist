module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  case map read (words inp) :: [Integer] of
    (n:rest) | n >= 1, not (null rest) -> do
      let xs = take (fromIntegral n) rest
          go (best, cur) x = (max best c, c) where c = max x (cur + x)
          (best, _) = foldl' go (head xs, head xs) (tail xs)
      putStrLn (show best)
    _ -> return ()