module Main where

import Data.Bits

dfs :: Int -> Int -> Int -> Int -> Int -> Int -> Int
dfs n full row cols diag1 diag2
    | row == n = 1
    | otherwise = go (full .&. complement (cols .|. diag1 .|. diag2))
  where
    go 0 = 0
    go available =
        let bit = available .&. negate available
            rest = available .&. (available - 1)
        in dfs n full (row + 1)
               (cols .|. bit)
               ((diag1 .|. bit) `shiftL` 1)
               ((diag2 .|. bit) `shiftR` 1)
           + go rest

main :: IO ()
main = do
    input <- getContents
    let n = read (head (words input)) :: Int
        full = (1 `shiftL` n) - 1
    print (dfs n full 0 0 0 0)