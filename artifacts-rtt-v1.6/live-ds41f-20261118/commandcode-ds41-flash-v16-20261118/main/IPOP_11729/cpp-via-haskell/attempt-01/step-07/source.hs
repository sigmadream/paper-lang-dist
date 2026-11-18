module Main where

import Data.Bits (shiftL)
import Data.ByteString.Builder
import System.IO (stdout, getContents, hPutBuilder)

hanoi :: Int -> Int -> Int -> Int -> Builder
hanoi n start middle end
    | n == 1 =
        intDec start <> charUtf8 ' ' <> intDec end <> charUtf8 '\n'
    | otherwise =
        hanoi (n - 1) start end middle
        <> intDec start <> charUtf8 ' ' <> intDec end <> charUtf8 '\n'
        <> hanoi (n - 1) middle start end

main :: IO ()
main = do
    input <- getContents
    let n = read (head (words input)) :: Int
        moves = (1 `shiftL` n) - 1
    hPutBuilder stdout (intDec moves <> charUtf8 '\n' <> hanoi n 1 2 3)