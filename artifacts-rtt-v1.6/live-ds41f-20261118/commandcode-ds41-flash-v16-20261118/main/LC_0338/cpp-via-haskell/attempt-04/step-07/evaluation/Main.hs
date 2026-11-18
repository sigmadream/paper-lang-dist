module Main where

import Data.Array (Array, listArray, (!))

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (x:_) -> do
      let n = read x :: Int
          counts :: Array Int Int
          counts = listArray (0, n) [f i | i <- [0..n]]
          f 0 = 0
          f i = counts ! (i `div` 2) + (i `mod` 2)
      putStrLn (unwords [show (counts ! i) | i <- [0..n]])