module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getContents
  case map read (words inp) :: [Integer] of
    (n:xs) | n > 0, length xs >= fromIntegral n ->
      let arr = take (fromIntegral n) xs
          go (c, b) x = let c' = max x (c + x) in (c', max b c')
          (_, best) = foldl' go (head arr, head arr) (tail arr)
      in print best
    _ -> return ()