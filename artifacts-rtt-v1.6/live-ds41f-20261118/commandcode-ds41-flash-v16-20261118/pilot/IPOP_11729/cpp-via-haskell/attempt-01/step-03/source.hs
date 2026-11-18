module Main where

import System.IO
import Data.Bits (shiftL)

hanoi :: Int -> Int -> Int -> Int -> IO ()
hanoi n s m e
    | n == 1 = putStrLn (show s ++ " " ++ show e)
    | otherwise = do
        hanoi (n - 1) s e m
        putStrLn (show s ++ " " ++ show e)
        hanoi (n - 1) m s e

main :: IO ()
main = do
    hSetBuffering stdout (BlockBuffering Nothing)
    n <- readLn :: IO Int
    print (((1 :: Int) `shiftL` n) - 1)
    hanoi n 1 2 3