module Main where

import Control.Monad (when, forM_)
import Control.Monad.ST (ST)
import Data.Array.ST (STUArray, newArray, readArray, writeArray, runSTUArray)
import Data.Array.Unboxed (UArray, (!))

sieveST :: Int -> ST s (STUArray s Int Bool)
sieveST n = do
    arr <- newArray (0, n) True
    writeArray arr 0 False
    when (n >= 1) $ writeArray arr 1 False
    let loop i
            | i * i > n = return ()
            | otherwise = do
                p <- readArray arr i
                when p $
                    forM_ [i * i, i * i + i .. n] $ \j ->
                        writeArray arr j False
                loop (i + 1)
    loop 2
    return arr

sieve :: Int -> UArray Int Bool
sieve n = runSTUArray (sieveST n)

main :: IO ()
main = do
    input <- getContents
    case (map read (words input) :: [Int]) of
        (m : n : _) -> do
            let primes = sieve n
            putStr $ unlines [show i | i <- [m .. n], primes ! i]
        _ -> return ()