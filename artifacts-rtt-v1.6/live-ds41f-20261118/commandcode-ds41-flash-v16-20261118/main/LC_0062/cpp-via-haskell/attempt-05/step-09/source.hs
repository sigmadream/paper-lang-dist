module Main where

import Data.List (foldl')

paths :: Integer -> Integer -> Integer
paths m n = last (foldl' (\row _ -> step row) (replicate (fromIntegral n) 1) [1 .. m - 1])
  where
    step [] = []
    step (x:xs) = x : go x xs

    go _ [] = []
    go acc (y:ys) =
      let z = y + acc
      in z : go z ys

main :: IO ()
main = do
  input <- getContents
  case map read (words input) :: [Integer] of
    (m:n:_) -> print (paths m n)
    _ -> return ()