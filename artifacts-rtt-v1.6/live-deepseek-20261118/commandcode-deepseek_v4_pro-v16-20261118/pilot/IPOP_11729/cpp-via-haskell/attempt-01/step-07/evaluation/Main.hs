module Main where

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
    line <- getLine
    let n = read line :: Int
    let moves = 2 ^ n - 1 :: Integer
    print moves
    mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) (hanoi n 1 2 3)