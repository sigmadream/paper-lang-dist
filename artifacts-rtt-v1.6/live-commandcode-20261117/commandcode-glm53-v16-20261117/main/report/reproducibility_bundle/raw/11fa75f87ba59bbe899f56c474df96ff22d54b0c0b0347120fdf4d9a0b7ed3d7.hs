module Main (main) where

import Data.List (foldl')

gcd' :: Integer -> Integer -> Integer
gcd' a 0 = a
gcd' a b = gcd' b (a `mod` b)

main :: IO ()
main = do
  line <- getLine
  let ws = words line
      a = read (head ws) :: Integer
      b = read (ws !! 1) :: Integer
      g = gcd' a b
  putStrLn (show g)
  putStrLn (show ((a `div` g) * b))