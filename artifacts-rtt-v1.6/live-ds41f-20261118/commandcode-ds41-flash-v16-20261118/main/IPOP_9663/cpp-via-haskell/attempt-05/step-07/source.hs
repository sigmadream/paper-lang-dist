{-# LANGUAGE BangPatterns #-}

module Main where

import Data.Bits

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (x:_) -> do
      let n = read x :: Int
          full = (1 `shiftL` n) - 1

          dfs :: Int -> Int -> Int -> Int -> Int
          dfs !row !cols !diag1 !diag2
            | row == n = 1
            | otherwise =
                let available = full .&. complement (cols .|. diag1 .|. diag2)
                    go !acc 0 = acc
                    go !acc a =
                      let !bit = a .&. negate a
                          !rest = a .&. (a - 1)
                          !acc' = acc + dfs
                            (row + 1)
                            (cols .|. bit)
                            ((diag1 .|. bit) `shiftL` 1)
                            ((diag2 .|. bit) `shiftR` 1)
                      in go acc' rest
                in go 0 available

      print (dfs 0 0 0 0)