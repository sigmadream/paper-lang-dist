module Main where

import Data.Array (Array, listArray, (!))
import Data.List (intercalate)
import System.IO (hSetBuffering, stdout, BufferMode(..))

main :: IO ()
main = do
    hSetBuffering stdout NoBuffering
    input <- getContents
    let tokens = words input
    if null tokens
        then return ()
        else do
            let n = read (head tokens) :: Int
                counts :: Array Int Int
                counts = listArray (0, n)
                    [ if i == 0 then 0 else counts ! (i `div` 2) + (i `mod` 2)
                    | i <- [0..n]
                    ]
                result = intercalate " " [show (counts ! i) | i <- [0..n]]
            putStrLn result