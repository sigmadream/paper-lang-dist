module Main where

import Data.Bits

main :: IO ()
main = do
  input <- getContents
  let n = read (head (words input)) :: Int
      full = (1 `shiftL` n) - 1
      go r cols d1 d2
        | r == n = 1
        | otherwise = loop (full .&. complement (cols .|. d1 .|. d2)) 0
        where
          loop 0 acc = acc
          loop avail acc =
            let b = avail .&. negate avail
                rest = avail `xor` b
                next = go (r + 1)
                          (cols .|. b)
                          (((d1 .|. b) `shiftL` 1) .&. full)
                          ((d2 .|. b) `shiftR` 1)
            in loop rest (acc + next)
  print (go 0 0 0 0)