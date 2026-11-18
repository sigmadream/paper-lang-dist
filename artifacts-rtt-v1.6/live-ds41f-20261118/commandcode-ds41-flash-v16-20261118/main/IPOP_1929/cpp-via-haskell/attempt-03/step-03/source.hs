module Main where

import Control.Monad (when)
import Control.Monad.ST (ST)
import Data.Array.ST (STUArray, newArray, readArray, runSTUArray, writeArray)
import Data.Array.Unboxed (UArray, (!))

sieve :: Int -> UArray Int Bool
sieve n = runSTUArray $ do
  arr <- newArray (0, n) True :: ST s (STUArray s Int Bool)
  when (n >= 0) $ writeArray arr 0 False
  when (n >= 1) $ writeArray arr 1 False

  let mark j
        | j > n = return ()
        | otherwise = do
            writeArray arr j False
            mark (j + i)
      loop i
        | i * i > n = return ()
        | otherwise = do
            p <- readArray arr i
            when p $ mark (i * i)
            loop (i + 1)

      loopWithI i
        | i * i > n = return ()
        | otherwise = do
            p <- readArray arr i
            when p $ do
              let mark' j
                    | j > n = return ()
                    | otherwise = do
                        writeArray arr j False
                        mark' (j + i)
              mark' (i * i)
            loopWithI (i + 1)

  loopWithI 2
  return arr

main :: IO ()
main = do
  input <- getContents
  case words input of
    (mStr : nStr : _) -> do
      let m = read mStr :: Int
          n = read nStr :: Int
          primes = sieve n
          result = [show i | i <- [m .. n], primes ! i]
      putStr (unlines result)
    _ -> return ()