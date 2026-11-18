module Main (main) where

import Data.Array (Array, listArray, (!), bounds)
import System.IO (hSetEncoding, stdout, utf8)

solve :: Int -> Array Int Int
solve n = arr
  where
    arr = listArray (0, n) [f i | i <- [0 .. n]]
    f i = if i == 0 then 0 else (arr ! (i `div` 2)) + (i `mod` 2)

main :: IO ()
main = do
    inp <- getContents
    let n = case words inp of
              (x:_) -> read x :: Int
              _     -> 0
    hSetEncoding stdout utf8
    let arr = solve n
    putStrLn $ unwords [show (arr ! i) | i <- [0 .. n]]