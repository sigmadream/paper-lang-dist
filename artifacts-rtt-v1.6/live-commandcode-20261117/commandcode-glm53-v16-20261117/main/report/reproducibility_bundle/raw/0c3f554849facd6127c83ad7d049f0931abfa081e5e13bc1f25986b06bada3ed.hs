module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)
import Data.Maybe (fromMaybe)

readInts :: IO [Integer]
readInts = do
  s <- BS.getContents
  return $ map (fromMaybe 0 . BS.readInteger) (BS.words s)

countGE :: [Integer] -> Integer -> Integer
countGE xs mid = go (tail xs) (head xs) 1
  where
    go [] _ cnt = cnt
    go (x:rest) prev cnt
      | x - prev >= mid = go rest x (cnt + 1)
      | otherwise = go rest prev cnt

main :: IO ()
main = do
  nums <- readInts
  let (n : c : rest) = nums
      a = sort (take (fromIntegral n) rest)
      lo = 1
      hi = last a - head a
      search l r ans
        | l > r = ans
        | countGE a mid >= c = search (mid + 1) r mid
        | otherwise = search l (mid - 1) ans
        where mid = l + (r - l) `div` 2
      ans = search lo hi 0
  print ans