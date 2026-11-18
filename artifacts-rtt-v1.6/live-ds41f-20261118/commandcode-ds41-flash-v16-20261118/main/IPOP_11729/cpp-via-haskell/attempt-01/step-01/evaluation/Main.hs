module Main where

import qualified Data.ByteString.Builder as B
import qualified Data.ByteString.Char8 as BS
import System.IO (stdout)

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
  input <- BS.getContents
  let s = BS.takeWhile (\c -> c /= ' ' && c /= '\n' && c /= '\r' && c /= '\t') input
  if BS.null s then return () else do
    let n = read (BS.unpack s) :: Int
        moves = hanoi n 1 2 3
        out = B.intDec (length moves) <> B.char8 '\n'
              <> foldMap (\(a, b) -> B.intDec a <> B.char8 ' ' <> B.intDec b <> B.char8 '\n') moves
    B.hPutBuilder stdout out