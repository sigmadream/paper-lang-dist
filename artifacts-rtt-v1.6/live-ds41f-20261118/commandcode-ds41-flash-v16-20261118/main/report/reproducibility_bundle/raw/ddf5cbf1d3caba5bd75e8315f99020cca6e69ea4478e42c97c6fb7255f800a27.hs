module Main where

import Data.Bits

solve :: Int -> Int
solve n = go 0 0 0 0
  where
    full = (1 `shiftL` n) - 1

    go :: Int -> Int -> Int -> Int -> Int
    go r cols d1 d2
      | r == n = 1
      | otherwise = loop avail
      where
        avail = full .&. complement (cols .|. d1 .|. d2)

        loop :: Int -> Int
        loop 0 = 0
        loop a =
          let b = a .&. negate a
              rest = a `xor` b
              nextCols = cols .|. b
              nextD1 = ((d1 .|. b) `shiftL` 1) .&. full
              nextD2 = (d2 .|. b) `shiftR` 1
          in go (r + 1) nextCols nextD1 nextD2 + loop rest

main :: IO ()
main = do
  input <- getContents
  let n = read (head (words input)) :: Int
  print (solve n)