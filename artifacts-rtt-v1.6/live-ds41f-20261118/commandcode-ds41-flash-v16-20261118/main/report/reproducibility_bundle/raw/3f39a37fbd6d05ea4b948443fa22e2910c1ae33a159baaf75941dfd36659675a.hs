module Main where

import Data.Bits

solve :: Int -> Int
solve n = dfs 0 0 0 0
  where
    full = (1 `shiftL` n) - 1

    dfs :: Int -> Int -> Int -> Int -> Int
    dfs row cols diag1 diag2
      | row == n = 1
      | otherwise = go (full .&. complement (cols .|. diag1 .|. diag2)) 0
      where
        go :: Int -> Int -> Int
        go 0 acc = acc
        go available acc =
          let bit = available .&. negate available
              nextAvailable = available .&. (available - 1)
              nextAcc = acc + dfs
                (row + 1)
                (cols .|. bit)
                ((diag1 .|. bit) `shiftL` 1)
                ((diag2 .|. bit) `shiftR` 1)
          in go nextAvailable nextAcc

main :: IO ()
main = do
  input <- getContents
  case words input of
    (x:_) -> print (solve (read x :: Int))
    _ -> return ()