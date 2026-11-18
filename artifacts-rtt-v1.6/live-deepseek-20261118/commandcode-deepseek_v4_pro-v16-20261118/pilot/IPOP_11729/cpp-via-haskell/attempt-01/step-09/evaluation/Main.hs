module Main where

import Text.Read (readMaybe)

hanoiMoves :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoiMoves 1 from _ to = [(from, to)]
hanoiMoves n from aux to =
    hanoiMoves (n-1) from to aux
    ++ [(from, to)]
    ++ hanoiMoves (n-1) aux from to

main :: IO ()
main = do
    input <- getLine
    case readMaybe input of
        Nothing -> return ()
        Just n -> do
            let total = (2 ^ n - 1 :: Integer)
            print total
            mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) (hanoiMoves n 1 2 3)