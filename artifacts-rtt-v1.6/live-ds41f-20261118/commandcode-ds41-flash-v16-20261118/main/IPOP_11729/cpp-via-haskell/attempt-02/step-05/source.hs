module Main where

import qualified Data.ByteString.Builder as B
import System.IO (stdout)
import Data.Bits (shiftL)

move :: Int -> Int -> B.Builder
move from to =
  B.intDec from <> B.string7 " " <> B.intDec to <> B.string7 "\n"

hanoi :: Int -> Int -> Int -> Int -> B.Builder
hanoi 0 _ _ _ = mempty
hanoi n from mid to
  | n == 1 = move from to
  | otherwise =
      hanoi (n - 1) from to mid
        <> move from to
        <> hanoi (n - 1) mid from to

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> pure ()
    (x:_) -> do
      let n = read x :: Int
          count = (1 `shiftL` n) - 1
      B.hPutBuilder stdout $
        B.intDec count <> B.string7 "\n" <> hanoi n 1 2 3