{-# LANGUAGE BangPatterns #-}

module Main where

import Data.Bits
import System.IO

queens :: Int -> Int
queens n = solve 0 0 0 0
  where
    full = (1 `shiftL` n) - 1

    solve :: Int -> Int -> Int -> Int -> Int
    solve !r !cols !d1 !d2
      | r == n = 1
      | otherwise = go (full .&. complement (cols .|. d1 .|. d2)) 0
      where
        go :: Int -> Int -> Int
        go 0 !acc = acc
        go bits !acc =
          let bit = bits .&. (-bits)
              acc' = acc + solve (r + 1)
                                 (cols .|. bit)
                                 ((d1 .|. bit) `shiftL` 1)
                                 ((d2 .|. bit) `shiftR` 1)
              bits' = bits .&. (bits - 1)
          in go bits' acc'

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (x:_) -> do
      let n = read x :: Int
      print (queens n)