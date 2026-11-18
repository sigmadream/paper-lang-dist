module Main where

import Control.Monad (forM_, when)
import Control.Monad.ST (ST, runST)
import Data.Array.ST (STUArray, newArray, readArray, writeArray, runSTUArray)
import Data.Array.Unboxed (UArray, (!))
import System.IO (getContents)

main :: IO ()
main = do
  s <- getContents
  case (map read (words s) :: [Int]) of
    (m : n : _) -> do
      let arr = sieve n :: UArray Int Int
          start = max 2 m
          res = [i | i <- [start .. n], arr ! i == 1]
      putStr (unlines (map show res))
    _ -> return ()

sieve :: Int -> UArray Int Int
sieve n = runSTUArray $ do
  arr <- newArray (0, n) 1 :: ST s (STUArray s Int Int)
  when (n >= 0) $ writeArray arr 0 0
  when (n >= 1) $ writeArray arr 1 0
  let lim = floor (sqrt (fromIntegral n)) :: Int
  forM_ [2 .. lim] $ \i -> do
    p <- readArray arr i
    when (p == 1) $ do
      let go j =
            when (j <= n) $ do
              writeArray arr j 0
              go (j + i)
      go (i * i)
  return arr