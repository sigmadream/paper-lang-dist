module Main (main) where

import System.IO

gcd' :: Integer -> Integer -> Integer
gcd' a 0 = a
gcd' a b = gcd' b (a `mod` b)

main :: IO ()
main = do
    hSetBuffering stdout LineBuffering
    input <- getLine
    let ws = words input
    case ws of
        (aStr:bStr:_) -> do
            let a = read aStr :: Integer
                b = read bStr :: Integer
                g = gcd' a b
            print g
            print ((a `div` g) * b)
        _ -> return ()