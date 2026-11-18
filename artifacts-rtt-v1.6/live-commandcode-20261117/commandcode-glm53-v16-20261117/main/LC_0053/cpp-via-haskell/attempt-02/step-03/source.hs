module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  let ws = map read (words inp) :: [Integer]
  case ws of
    (n:rest) | n >= 1 ->
      let xs = take (fromIntegral n) rest
          go (best, cur) x = (max best c, c) where c = max x (cur + x)
          (b, _) = foldl' go (head xs, head xs) (tail xs)
      in print b
    _ -> return ()