module Main where

import System.IO

hanoi :: Int -> Int -> Int -> Int -> Handle -> IO ()
hanoi n start mid end h
    | n == 1 = hPutStrLn h (show start ++ " " ++ show end)
    | otherwise = do
        hanoi (n - 1) start end mid h
        hPutStrLn h (show start ++ " " ++ show end)
        hanoi (n - 1) mid start end h

main :: IO ()
main = do
    hSetBuffering stdout (BlockBuffering Nothing)
    input <- getLine
    let n = read input :: Int
    print ((2 ^ n) - 1)
    hanoi n 1 2 3 stdout