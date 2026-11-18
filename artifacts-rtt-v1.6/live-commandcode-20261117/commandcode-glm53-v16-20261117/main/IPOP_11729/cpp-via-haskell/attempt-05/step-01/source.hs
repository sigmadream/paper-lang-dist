module Main (main) where

import System.IO

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
    inp <- getLine
    let n = read inp :: Int
    let moves = hanoi n 1 2 3
    mapM_ putStrLn ((show (length moves) : map (\(a, b) -> show a ++ " " ++ show b) moves))