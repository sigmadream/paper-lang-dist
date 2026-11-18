module Main (main) where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)
import Data.Maybe (fromMaybe)

readInts :: IO [Integer]
readInts = do
  contents <- BS.getContents
  return $ map (maybe 0 fst . BS.readInteger) (BS.words contents)

countGE :: [Integer] -> Integer -> Integer
countGE s mid
  | null s = 0
  | otherwise = go (tail s) (head s) 1
  where
    go [] _ k = k
    go (x:xs) prev k
      | x - prev >= mid = go xs x (k + 1)
      | otherwise = go xs prev k

search_ :: [Integer] -> Integer -> Integer -> Integer -> Integer -> Integer
search_ s c lo hi acc
  | lo > hi = acc
  | countGE s mid >= c = search_ s c (mid + 1) hi mid
  | otherwise = search_ s c lo (mid - 1) acc
  where
    mid = lo + (hi - lo) `div` 2

main :: IO ()
main = do
  nums <- readInts
  case nums of
    (n:c:rest) -> do
      let a = take (fromIntegral n) rest
          s = sort a
          lo = 1
          hi = last s - head s
      print (search_ s c lo hi 0)
    _ -> return ()