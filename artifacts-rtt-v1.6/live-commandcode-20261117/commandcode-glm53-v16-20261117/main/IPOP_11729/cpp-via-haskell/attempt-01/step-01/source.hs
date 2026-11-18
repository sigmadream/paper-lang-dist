module Main (main) where

import Data.List (intercalate)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
    inp <- getContents
    let ns = words inp
    case ns of
        (x:_) | n <- read x :: Int, n >= 1 -> do
            let moves = hanoi n 1 2 3
            putStrLn (show (length moves))
            mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves
        _ -> return ()