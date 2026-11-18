module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)

readInts :: IO [Int]
readInts = do
  s <- BS.getContents
  return $ map readInt (BS.words s)

readInt :: BS.ByteString -> Int
readInt = maybe 0 fst . BS.readInt

main :: IO ()
main = do
  xs <- readInts
  case xs of
    (n:c:rest) -> do
      let a = take n rest
          s = sort a
          lo = 1
          hi = last s - head s
          ans = search s c lo hi 0
      print ans
    _ -> return ()

search :: [Int] -> Int -> Int -> Int -> Int -> Int
search s c lo hi acc
  | lo > hi = acc
  | otherwise =
      let mid = lo + (hi - lo) `div` 2
          cnt = countGE s mid
      in if cnt >= c
           then search s c (mid + 1) hi mid
           else search s c lo (mid - 1) acc

countGE :: [Int] -> Int -> Int
countGE (x:xs) mid = go xs x 1
  where
    go [] _ k = k
    go (y:ys) prev k
      | y - prev >= mid = go ys y (k + 1)
      | otherwise = go ys prev k
countGE [] _ = 0