module Main (main) where

import Data.Array (Array, listArray, (!))
import qualified Data.ByteString.Char8 as BS

main :: IO ()
main = do
  inp <- BS.getContents
  let n = case BS.readInteger (BS.dropWhile (== ' ') inp) of
            Just (v, _) -> v
            Nothing     -> 0
      cnts :: Array Integer Int
      cnts = listArray (0, n) (0 : map f [1 .. n])
      f i = cnts ! (i `div` 2) + fromIntegral (i `mod` 2)
  putStrLn (unwords [show (cnts ! i) | i <- [0 .. n]])