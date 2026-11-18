module Main where

import Data.Array

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (x:_) -> do
            let n = read x :: Int
                counts = listArray (0, n)
                    [ if i == 0 then 0 else counts ! (i `div` 2) + (i `mod` 2)
                    | i <- [0..n]
                    ]
                result = unwords [show (counts ! i) | i <- [0..n]]
            putStrLn result