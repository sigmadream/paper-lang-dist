module Main where

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (x:_) -> do
            let n = read x :: Int
                moves = hanoi n 1 2 3 []
                count = (2 :: Int) ^ n - 1
            putStrLn (show count)
            putStr (concatMap (\(a, b) -> show a ++ " " ++ show b ++ "\n") moves)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)] -> [(Int, Int)]
hanoi 0 _ _ _ k = k
hanoi 1 a _ c k = (a, c) : k
hanoi n a b c k =
    hanoi (n - 1) a c b ((a, c) : hanoi (n - 1) b a c k)