module Main where

import Data.List (foldl')

main :: IO ()
main = do
    input <- getContents
    let (m:n:_) = map read (words input) :: [Int]
        dp0 = replicate n 1
        step dp = scanl (+) 1 (drop 1 dp)
        dp = foldl' (\acc _ -> step acc) dp0 [1..m-1]
    print (last dp)