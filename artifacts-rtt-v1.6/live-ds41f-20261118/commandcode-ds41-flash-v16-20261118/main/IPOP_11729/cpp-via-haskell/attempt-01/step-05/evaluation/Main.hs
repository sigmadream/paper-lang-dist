module Main where

import System.IO (hSetBuffering, stdout, BufferMode(..))

hanoi :: Int -> Int -> Int -> Int -> ShowS
hanoi 1 start _ end =
    shows start . showChar ' ' . shows end . showChar '\n'
hanoi n start middle end =
    hanoi (n - 1) start end middle .
    shows start . showChar ' ' . shows end . showChar '\n' .
    hanoi (n - 1) middle start end

main :: IO ()
main = do
    hSetBuffering stdout (BlockBuffering Nothing)
    input <- getLine
    let n = read input :: Int
    putStrLn (show ((2 ^ n) - 1 :: Int))
    putStr (hanoi n 1 2 3 "")