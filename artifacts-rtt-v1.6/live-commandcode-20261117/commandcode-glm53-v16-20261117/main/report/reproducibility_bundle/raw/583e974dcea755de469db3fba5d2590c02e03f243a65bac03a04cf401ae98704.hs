module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)

readInts :: IO [Int]
readInts = do
  inp <- BS.getContents
  return $ map (maybe 0 fst . BS.readInt) (BS.words inp)

main :: IO ()
main = do
  (n:c:xs) <- readInts
  let s = sort (take n xs)
      lo0 = 1
      hi0 = last s - head s
      feasible mid = go 1 (head s) (tail s) >= c
        where
          go k p (y:ys) | y - p >= mid = go (k+1) y ys
                        | otherwise    = go k p ys
          go k _ [] = k
      bin lo hi ans
        | lo > hi = ans
        | feasible mid = bin (mid+1) hi mid
        | otherwise = bin lo (mid-1) ans
        where mid = lo + (hi - lo) `div` 2
      ans = bin lo0 hi0 0
  print ans