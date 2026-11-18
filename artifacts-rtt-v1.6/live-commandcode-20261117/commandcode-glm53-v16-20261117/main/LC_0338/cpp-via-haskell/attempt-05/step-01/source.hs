module Main (main) where

import Data.Char (isDigit)
import qualified Data.ByteString.Char8 as BS

main :: IO ()
main = do
  input <- BS.getContents
  let n = readInt input
      counts = 0 : map f [1 .. n]
      f i = counts !! (i `div` 2) + (i `mod` 2)
  putStrLn (unwords (map show counts))

readInt :: BS.ByteString -> Int
readInt s =
  let t = BS.dropWhile (not . isDigit) s
      (d, _) = BS.span isDigit t
  in case BS.readInt d of
       Just (v, _) -> v
       Nothing -> 0