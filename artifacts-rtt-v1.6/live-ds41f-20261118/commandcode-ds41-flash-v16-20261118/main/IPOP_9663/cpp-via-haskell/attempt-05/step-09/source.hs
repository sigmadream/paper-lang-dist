module Main where

import Data.Bits (complement, (.&.), (.|.), shiftL, shiftR)
import System.IO

dfs :: Int -> Int -> Int -> Int -> Int -> Int -> Int
dfs n fullMask row cols diag1 diag2
    | row == n = 1
    | otherwise = go available 0
  where
    available = fullMask .&. complement (cols .|. diag1 .|. diag2)

    go 0 total = total
    go bits total =
        let bit = bits .&. negate bits
            next = bits .&. (bits - 1)
            total' = total + dfs
                n
                fullMask
                (row + 1)
                (cols .|. bit)
                ((diag1 .|. bit) `shiftL` 1)
                ((diag2 .|. bit) `shiftR` 1)
        in go next total'

main :: IO ()
main = do
    input <- getContents
    let values = map read (words input) :: [Int]
    case values of
        (n:_) -> do
            let fullMask = (1 `shiftL` n) - 1
            print (dfs n fullMask 0 0 0 0)
        _ -> return ()