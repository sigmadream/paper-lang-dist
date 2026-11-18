module Main where

import Control.Monad (forM_, when)
import Control.Monad.ST (runST)
import Data.Array.ST (STUArray, newArray, readArray, writeArray)

main :: IO ()
main = do
  input <- getContents
  let numbers = map read (words input) :: [Int]
  case numbers of
    (m:n:_) -> mapM_ print (primesInRange m n)
    _ -> return ()

primesInRange :: Int -> Int -> [Int]
primesInRange m n = runST $ do
  isPrime <- newArray (0, n) True :: STUArray s Int Bool

  writeArray isPrime 0 False
  when (n >= 1) $ writeArray isPrime 1 False

  let limit = floor (sqrt (fromIntegral n :: Double)) :: Int

  forM_ [2 .. limit] $ \i -> do
    prime <- readArray isPrime i
    when prime $
      forM_ [i * i, i * i + i .. n] $ \j ->
        writeArray isPrime j False

  flags <- mapM (readArray isPrime) [m .. n]
  return [x | (x, flag) <- zip [m .. n] flags, flag]