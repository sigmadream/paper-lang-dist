module Main (main) where

import Data.List (intercalate)
import System.IO

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
    inp <- getContents
    let ls = lines inp
        ns = ls >>= words
    case ns of
        (x:_) -> do
            let n = read x :: Int
                moves = hanoi n 1 2 3
            putStrLn (show (length moves))
            mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves
        [] -> return ()