module Main (main) where

import Data.Bits (shiftL)
import Data.Char (isDigit)
import qualified Data.ByteString.Char8 as BS

hanoi :: Int -> Int -> Int -> Int -> [(Int, Int)]
hanoi 1 s _ e = [(s, e)]
hanoi n s m e = hanoi (n - 1) s e m ++ [(s, e)] ++ hanoi (n - 1) m s e

main :: IO ()
main = do
  input <- BS.getContents
  let n = read (takeWhile isDigit (BS.unpack input)) :: Int
      cnt = (2 ^ n) - 1 :: Integer
  putStrLn (show cnt)
  mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) (hanoi n 1 2 3)