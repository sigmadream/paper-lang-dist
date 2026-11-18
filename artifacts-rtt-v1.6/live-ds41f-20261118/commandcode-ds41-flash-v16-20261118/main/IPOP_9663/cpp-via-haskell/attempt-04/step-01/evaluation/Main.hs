module Main where

import Data.Bits
import System.IO

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (x:_) -> do
            let n = read x :: Int
            print (countQueens n)

countQueens :: Int -> Int
countQueens n = go 0 0 0 0
  where
    go r cols diag1 diag2
        | r == n = 1
        | otherwise = loop 0 0
      where
        loop c acc
            | c == n = acc
            | otherwise =
                let bitCol = 1 `shiftL` c
                    bitDiag1 = 1 `shiftL` (r + c)
                    bitDiag2 = 1 `shiftL` (r - c + n - 1)
                in if (cols .&. bitCol) /= 0
                      || (diag1 .&. bitDiag1) /= 0
                      || (diag2 .&. bitDiag2) /= 0
                   then loop (c + 1) acc
                   else loop (c + 1) (acc + go (r + 1)
                                               (cols .|. bitCol)
                                               (diag1 .|. bitDiag1)
                                               (diag2 .|. bitDiag2))