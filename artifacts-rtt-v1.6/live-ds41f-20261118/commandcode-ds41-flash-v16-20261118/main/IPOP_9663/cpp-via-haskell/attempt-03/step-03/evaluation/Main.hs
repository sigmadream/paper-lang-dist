module Main where

import Data.Bits (complement, shiftL, shiftR, xor, (.&.), (.|.))

countQueens :: Int -> Int
countQueens n = go 0 0 0 0
  where
    full = (1 `shiftL` n) - 1

    go r cols diag1 diag2
      | r == n = 1
      | otherwise = loop (full .&. complement (cols .|. diag1 .|. diag2)) 0
      where
        loop available acc
          | available == 0 = acc
          | otherwise =
              let bit = available .&. (-available)
                  rest = available `xor` bit
                  nextDiag1 = ((diag1 .|. bit) `shiftL` 1) .&. full
                  nextDiag2 = (diag2 .|. bit) `shiftR` 1
              in loop rest (acc + go (r + 1) (cols .|. bit) nextDiag1 nextDiag2)

main :: IO ()
main = do
  input <- getContents
  case words input of
    (x:_) -> print (countQueens (read x :: Int))
    [] -> return ()