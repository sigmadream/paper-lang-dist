module Main (main) where

import Data.Bits (shiftL)
import Data.ByteString.Builder (Builder, char7, hPutBuilder, intDec)
import System.IO (BufferMode (BlockBuffering), hSetBuffering, stdout)

hanoi :: Int -> Int -> Int -> Int -> Builder
hanoi n from mid to
  | n == 1 =
      intDec from <> char7 ' ' <> intDec to <> char7 '\n'
  | otherwise =
      hanoi (n - 1) from to mid
        <> intDec from <> char7 ' ' <> intDec to <> char7 '\n'
        <> hanoi (n - 1) mid from to

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (x:_) -> do
      let n = read x :: Int
      hSetBuffering stdout (BlockBuffering Nothing)
      hPutBuilder stdout $
        intDec (((1 :: Int) `shiftL` n) - 1)
          <> char7 '\n'
          <> hanoi n 1 2 3