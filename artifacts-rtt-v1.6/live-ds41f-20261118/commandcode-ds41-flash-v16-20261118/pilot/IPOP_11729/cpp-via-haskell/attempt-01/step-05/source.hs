module Main where

hanoi :: Int -> Int -> Int -> Int -> String
hanoi n s m e
    | n == 1 = show s ++ " " ++ show e ++ "\n"
    | otherwise =
        hanoi (n - 1) s e m
        ++ show s ++ " " ++ show e ++ "\n"
        ++ hanoi (n - 1) m s e

main :: IO ()
main = do
    input <- getLine
    let n = read input :: Int
    putStrLn (show ((1 `shiftL` n) - 1))
    putStr (hanoi n 1 2 3)
  where
    shiftL x k = x * (2 ^ k)