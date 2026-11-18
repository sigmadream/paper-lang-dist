module Main where

import System.IO

hanoi :: Int -> Int -> Int -> Int -> IO ()
hanoi 0 _ _ _ = pure ()
hanoi n from via to = do
    hanoi (n - 1) from to via
    putStrLn (show from ++ " " ++ show to)
    hanoi (n - 1) via from to

main :: IO ()
main = do
    hSetBuffering stdout (BlockBuffering Nothing)
    contents <- getContents
    let n = read (head (words contents)) :: Int
        moves = (2 ^ n - 1) :: Int
    print moves
    hanoi n 1 2 3