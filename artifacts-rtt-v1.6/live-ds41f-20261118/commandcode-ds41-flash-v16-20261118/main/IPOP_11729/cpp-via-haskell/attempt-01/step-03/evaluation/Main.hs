module Main where

import qualified Data.ByteString.Builder as B
import qualified Data.ByteString.Lazy as L
import System.IO (stdout)

hanoi :: Int -> Int -> Int -> Int -> B.Builder
hanoi 1 start _ end =
    B.intDec start <> B.char8 ' ' <> B.intDec end <> B.char8 '\n'
hanoi n start middle end =
    hanoi (n - 1) start end middle <>
    B.intDec start <> B.char8 ' ' <> B.intDec end <> B.char8 '\n' <>
    hanoi (n - 1) middle start end

main :: IO ()
main = do
    input <- getContents
    let n = read (head (words input)) :: Int
        moves = (2 :: Integer) ^ n - 1
    L.hPut stdout $
        B.toLazyByteString $
            B.integerDec moves <> B.char8 '\n' <> hanoi n 1 2 3