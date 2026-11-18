module Main where

import Data.Bits
import System.IO

countQueens :: Int -> Int
countQueens n = go 0 0 0 0
  where
    full = (1 `shiftL` n) - 1

    go :: Int -> Int -> Int -> Int -> Int
    go r cols diag1 diag2
      | r == n = 1
      | otherwise = loop available 0
      where
        available = full .&. complement (cols .|. diag1 .|. diag2)

        loop :: Int -> Int -> Int
        loop 0 acc = acc
        loop bits acc =
          let bit = bits .&. negate bits
              rest = bits `xor` bit
              nextCols = cols .|. bit
              nextDiag1 = ((diag1 .|. bit) `shiftL` 1) .&. full
              nextDiag2 = (diag2 .|. bit) `shiftR` 1
              acc' = acc + go (r + 1) nextCols nextDiag1 nextDiag2
          in loop rest acc'

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (x:_) -> do
      let n = read x :: Int
      print (countQueens n)