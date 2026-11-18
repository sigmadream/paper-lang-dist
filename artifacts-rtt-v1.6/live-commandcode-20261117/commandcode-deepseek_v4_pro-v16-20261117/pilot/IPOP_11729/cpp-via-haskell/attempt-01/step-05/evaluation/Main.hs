module Main where

import Text.Read (readMaybe)

hanoiMoves :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoiMoves 1 from _ to = [(from, to)]
hanoiMoves n from mid to =
    hanoiMoves (n-1) from to mid ++
    [(from, to)] ++
    hanoiMoves (n-1) mid from to

main :: IO ()
main = do
    input <- getLine
    case readMaybe input :: Maybe Int of
        Nothing -> return ()
        Just n
            | n < 1 || n > 20 -> return ()
            | otherwise -> do
                let count = 2 ^ n - 1 :: Integer
                putStrLn (show count)
                let moves = hanoiMoves n 1 2 3
                putStr (unlines (map (\(a, b) -> show a ++ " " ++ show b) moves))