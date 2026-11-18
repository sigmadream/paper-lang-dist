module Main (main) where

import System.IO

gcd' :: Integer -> Integer -> Integer
gcd' a b
  | b == 0 = a
  | otherwise = gcd' b (a `mod` b)

main :: IO ()
main = do
  line <- getLine
  case map read (words line) of
    [a, b] -> do
      let g = gcd' a b
      print g
      print ((a `div` g) * b)
    _ -> return ()