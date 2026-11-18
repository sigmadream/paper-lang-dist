module Main where

import Control.Monad (forM_, when)
import Control.Monad.ST (ST, runST)
import Data.Array.ST (STUArray, newArray, readArray, writeArray)

main :: IO ()
main = do
  contents <- getContents
  case words contents of
    (a:b:_) -> do
      let m = read a :: Int
          n = read b :: Int
      mapM_ print (filter (>= m) (sieve n))
    _ -> return ()

sieve :: Int -> [Int]
sieve n
  | n < 2 = []
  | otherwise = runST (sieveST n)

sieveST :: Int -> ST s [Int]
sieveST n = do
  isPrime <- newArray (0, n) True :: ST s (STUArray s Int Bool)
  writeArray isPrime 0 False
  writeArray isPrime 1 False

  let limit = floor (sqrt (fromIntegral n :: Double)) :: Int
  forM_ [2 .. limit] $ \i -> do
    p <- readArray isPrime i
    when p $
      forM_ [i * i, i * i + i .. n] $ \j ->
        writeArray isPrime j False

  let collect i acc
        | i > n = return (reverse acc)
        | otherwise = do
            p <- readArray isPrime i
            collect (i + 1) (if p then i : acc else acc)

  collect 2 []