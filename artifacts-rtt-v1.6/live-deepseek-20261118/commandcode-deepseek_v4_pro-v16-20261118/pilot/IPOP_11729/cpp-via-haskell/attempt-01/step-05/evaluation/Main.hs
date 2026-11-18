module Main where

main :: IO ()
main = do
    n <- readLn :: IO Int
    putStrLn $ show (2^n - 1 :: Integer)
    hanoi n 1 2 3

hanoi :: Int -> Int -> Int -> Int -> IO ()
hanoi n start mid end
    | n == 1 = putStrLn $ show start ++ " " ++ show end
    | otherwise = do
        hanoi (n - 1) start end mid
        putStrLn $ show start ++ " " ++ show end
        hanoi (n - 1) mid start end