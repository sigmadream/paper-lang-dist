module Main where

import Data.Array (listArray, (!), elems)

main :: IO ()
main = do
  input <- getContents
  let n = read (head (words input)) :: Int
      counts = listArray (0, n) (0 : [counts ! (i `div` 2) + i `mod` 2 | i <- [1 .. n]])
  putStrLn (unwords (map show (elems counts)))