module Main where

import Control.Monad (when)
import Data.Array.ST (newArray, readArray, writeArray, runSTUArray)
import Data.Array.Unboxed (UArray, (!))

main :: IO ()
main = do
  input <- getContents
  case map read (words input) :: [Int] of
    (m:n:_) -> do
      let arr = sieve n
          start = max 2 m
          result = [i | i <- [start..n], arr ! i]
      putStr (unlines (map show result))
    _ -> return ()

sieve :: Int -> UArray Int Bool
sieve n = runSTUArray $ do
  arr <- newArray (0, n) True
  when (n >= 0) $ writeArray arr 0 False
  when (n >= 1) $ writeArray arr 1 False

  let mark i j
        | j > n = return ()
        | otherwise = do
            writeArray arr j False
            mark i (j + i)

      loop i
        | i * i > n = return ()
        | otherwise = do
            isPrime <- readArray arr i
            when isPrime $ mark i (i * i)
            loop (i + 1)

  loop 2
  return arr