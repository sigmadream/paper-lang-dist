module Main (main) where

import Data.List (intercalate)

main :: IO ()
main = do
  n <- readLn :: IO Int
  let counts = go [0 .. n]
      go [] = []
      go (i:is)
        | i == 0 = 0 : go is
        | otherwise = (counts !! (i `div` 2) + i `mod` 2) : go is
  -- avoid recomputation: build iteratively
  let arr = 0 : [ (arr !! (i `div` 2)) + (i `mod` 2) | i <- [1 .. n] ]
  putStrLn $ intercalate " " (map show arr)