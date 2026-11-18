module Main where

import qualified Data.ByteString.Builder as B
import System.IO (stdout, hPutBuilder)

hanoi :: Int -> Int -> Int -> Int -> B.Builder
hanoi 0 _ _ _ = mempty
hanoi n f v t =
  hanoi (n - 1) f t v <>
  B.intDec f <> B.char7 ' ' <> B.intDec t <> B.char7 '\n' <>
  hanoi (n - 1) v f t

main :: IO ()
main = do
  s <- getContents
  case words s of
    [] -> return ()
    (x:_) -> do
      let n = read x :: Int
      hPutBuilder stdout (B.intDec ((2 ^ n) - 1) <> B.char7 '\n' <> hanoi n 1 2 3)