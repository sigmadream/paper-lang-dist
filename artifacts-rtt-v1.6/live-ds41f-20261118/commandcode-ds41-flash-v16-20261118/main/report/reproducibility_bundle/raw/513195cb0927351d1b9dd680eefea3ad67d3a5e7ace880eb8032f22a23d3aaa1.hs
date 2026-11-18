module Main where

import Control.Monad (forM_, when)
import Control.Monad.ST (ST)
import Data.Array.ST (STUArray, newArray, readArray, runSTUArray, writeArray)
import Data.Array.Unboxed ((!))

main :: IO ()
main = do
    input <- getContents
    case map read (words input) :: [Int] of
        (m : n : _) ->
            let isPrime = sieve n
            in putStr $ unlines [show i | i <- [m .. n], isPrime ! i]
        _ -> return ()

sieve :: Int -> Data.Array.Unboxed.UArray Int Bool
sieve n = runSTUArray $ do
    arr <- newArray (0, n) True :: ST s (STUArray s Int Bool)
    when (n >= 0) $ writeArray arr 0 False
    when (n >= 1) $ writeArray arr 1 False
    let limit = (floor (sqrt (fromIntegral n :: Double))) :: Int
    forM_ [2 .. limit] $ \i -> do
        p <- readArray arr i
        when p $ forM_ [i * i, i * i + i .. n] $ \j ->
            writeArray arr j False
    return arr