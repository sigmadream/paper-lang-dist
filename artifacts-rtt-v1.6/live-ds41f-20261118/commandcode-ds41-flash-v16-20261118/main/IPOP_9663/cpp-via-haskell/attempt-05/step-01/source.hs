{-# LANGUAGE BangPatterns #-}

module Main where

import Data.Bits

main :: IO ()
main = do
    input <- getContents
    let n = read (head (words input)) :: Int
    print (queens n)

queens :: Int -> Int
queens n = go 0 0 0 0
  where
    full = (1 `shiftL` n) - 1

    go :: Int -> Int -> Int -> Int -> Int
    go !r !cols !diag1 !diag2
        | r == n = 1
        | otherwise = loop (full .&. complement (cols .|. diag1 .|. diag2)) 0
      where
        loop :: Int -> Int -> Int
        loop 0 !acc = acc
        loop mask !acc =
            let b = mask .&. negate mask
                acc' = acc + go
                    (r + 1)
                    (cols .|. b)
                    ((diag1 .|. b) `shiftL` 1)
                    ((diag2 .|. b) `shiftR` 1)
            in loop (mask .&. (mask - 1)) acc'