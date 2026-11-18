module Main (main) where

import Data.List (foldl')

main :: IO ()
main = do
  inp <- getLine
  case map read (words inp) :: [Integer] of
    [m, n] -> print (uniquePaths m n)
    _ -> return ()

uniquePaths :: Integer -> Integer -> Integer
uniquePaths m n = last row
  where
    row = iterate step (replicate (fromInteger n) 1) !! (fromInteger m - 1)
    step xs = 1 : zipWith (+) xs (tail' xs)
    tail' (_:ys) = ys
    tail' [] = []