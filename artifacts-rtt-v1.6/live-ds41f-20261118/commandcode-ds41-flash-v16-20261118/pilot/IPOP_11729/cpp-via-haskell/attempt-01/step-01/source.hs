module Main where

import Data.Bits (shiftL)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e =
    hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
    input <- getLine
    let n = read input :: Int
    let moves = hanoi n 1 2 3
    putStrLn (show (((1 :: Int) `shiftL` n) - 1))
    putStr (unlines [show a ++ " " ++ show b | (a, b) <- moves])