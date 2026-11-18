module Main where

import Control.Monad (when)
import Data.Array.ST (STUArray, newArray, readArray, runSTUArray, writeArray)
import Data.Array.Unboxed (UArray, (!))

sieve :: Int -> UArray Int Bool
sieve n = runSTUArray $ do
  isPrime <- newArray (0, n) True
  when (n >= 0) $ writeArray isPrime 0 False
  when (n >= 1) $ writeArray isPrime 1 False
  let mark p j
        | j > n = return ()
        | otherwise = do
            writeArray isPrime j False
            mark p (j + p)
      loop i
        | i * i > n = return ()
        | otherwise = do
            p <- readArray isPrime i
            when p $ mark i (i * i)
            loop (i + 1)
  loop 2
  return isPrime

main :: IO ()
main = do
  input <- getContents
  case map read (words input) :: [Int] of
    (m:n:_) -> do
      let primes = sieve n
      putStr $ unlines [show i | i <- [m .. n], primes ! i]
    _ -> return ()