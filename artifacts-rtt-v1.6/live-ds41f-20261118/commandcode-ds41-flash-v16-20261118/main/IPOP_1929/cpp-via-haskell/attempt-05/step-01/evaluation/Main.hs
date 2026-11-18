{-# LANGUAGE ScopedTypeVariables #-}

module Main (main) where

import Control.Monad (when)
import Control.Monad.ST (ST, runST)
import Data.Array.ST (STUArray, newArray, readArray, writeArray)

main :: IO ()
main = do
    input <- getContents
    case words input of
        (ms:ns:_) -> do
            let m = read ms :: Int
                n = read ns :: Int
            putStr $ unlines $ map show (primesIn m n)
        _ -> return ()

primesIn :: Int -> Int -> [Int]
primesIn m n = runST action
  where
    action :: forall s. ST s [Int]
    action = do
        isPrime <- newArray (0, n) True :: ST s (STUArray s Int Bool)
        writeArray isPrime 0 False
        writeArray isPrime 1 False

        let mark j step
                | j > n = return ()
                | otherwise = do
                    writeArray isPrime j False
                    mark (j + step) step

            sieve i
                | i * i > n = return ()
                | otherwise = do
                    p <- readArray isPrime i
                    when p $ mark (i * i) i
                    sieve (i + 1)

            collect i acc
                | i > n = return (reverse acc)
                | otherwise = do
                    b <- readArray isPrime i
                    collect (i + 1) (if b then i : acc else acc)

        sieve 2
        collect m []