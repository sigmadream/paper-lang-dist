module Main (main) where

import Data.Array

main :: IO ()
main = do
  n <- readLn :: IO Int
  let arr = listArray (0, n) [ f i | i <- [0 .. n] ]
      f 0 = 0
      f i = arr ! (i `div` 2) + i `mod` 2
  putStrLn $ unwords (map show [ arr ! i | i <- [0 .. n] ])