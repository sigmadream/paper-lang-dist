module Main (main) where

import System.IO

main :: IO ()
main = do
  inp <- getLine
  case map read (words inp) of
    (a : b : _) -> do
      let g = gcd a b
      print g
      print ((a `div` g) * b)
    _ -> return ()