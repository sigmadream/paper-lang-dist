module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)

main :: IO ()
main = do
  inp <- BS.getContents
  let (n : c : rest) = map (maybe 0 fst . BS.readInteger) (BS.words inp)
      s = sort (take (fromIntegral n) rest)
      countGE mid = go 1 (head s) (tail s)
        where
          go k _ [] = k
          go k p (x:xs)
            | x - p >= mid = go (k+1) x xs
            | otherwise = go k p xs
      search lo hi acc
        | lo > hi = acc
        | countGE mid >= c = search (mid+1) hi mid
        | otherwise = search lo (mid-1) acc
        where mid = lo + (hi - lo) `div` 2
  print (search 1 (last s - head s) 0)