module Main (main) where

import System.IO

hanoi :: Int -> Int -> Int -> Int -> [String]
hanoi 1 s _ e = [show s ++ " " ++ show e]
hanoi n s m e = hanoi (n - 1) s e m ++ [show s ++ " " ++ show e] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
    n <- readLn :: IO Int
    let cnt = (2 ^ n) - 1 :: Integer
    putStr $ unlines (show cnt : hanoi n 1 2 3)