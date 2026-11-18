module Main where

import Control.Monad (when)
import Control.Monad.ST (ST, runST)
import Data.Array.ST (STUArray, newArray, readArray, writeArray)

sieveRange :: Int -> Int -> [Int]
sieveRange m n = runST $ do
  isPrime <- newArray (0, n) True :: ST s (STUArray s Int Bool)

  when (n >= 0) $ writeArray isPrime 0 False
  when (n >= 1) $ writeArray isPrime 1 False

  let loop i
        | i * i > n = return ()
        | otherwise = do
            p <- readArray isPrime i
            when p $ do
              let mark j
                    | j > n = return ()
                    | otherwise = do
                        writeArray isPrime j False
                        mark (j + i)
              mark (i * i)
            loop (i + 1)

  loop 2

  bs <- mapM (readArray isPrime) [m .. n]
  return [i | (i, True) <- zip [m .. n] bs]

main :: IO ()
main = do
  input <- getContents
  case map read (words input) :: [Int] of
    (m : n : _) -> mapM_ print (sieveRange m n)
    _ -> return ()