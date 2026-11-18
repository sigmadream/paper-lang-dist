module Main (main) where

import System.IO

gcd' :: Int -> Int -> Int
gcd' a 0 = a
gcd' a b = gcd' b (a `mod` b)

main :: IO ()
main = do
    contents <- getContents
    case map read (words contents) :: [Int] of
        (a:b:_) -> do
            let g = gcd' a b
            putStrLn (show g)
            putStrLn (show ((a `div` g) * b))
        _ -> return ()