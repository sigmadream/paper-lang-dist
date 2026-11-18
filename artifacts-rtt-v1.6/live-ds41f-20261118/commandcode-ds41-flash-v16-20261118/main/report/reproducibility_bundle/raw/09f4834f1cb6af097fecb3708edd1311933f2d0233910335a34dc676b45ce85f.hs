module Main where

import qualified Data.ByteString.Lazy.Char8 as BS
import Data.List (sort)

toInt :: BS.ByteString -> Int
toInt bs =
  case BS.readInt bs of
    Just (x, _) -> x
    Nothing -> 0

main :: IO ()
main = do
  input <- BS.getContents
  let nums = map toInt (BS.words input)
  case nums of
    (n:c:rest) -> do
      let houses = sort (take n rest)
          lo = 1
          hi = last houses - head houses
          answer = search houses c lo hi 0
      print answer
    _ -> return ()

search :: [Int] -> Int -> Int -> Int -> Int -> Int
search houses c lo hi best
  | lo > hi = best
  | otherwise =
      let mid = lo + (hi - lo) `div` 2
      in if canPlace houses c mid
           then search houses c (mid + 1) hi mid
           else search houses c lo (mid - 1) best

canPlace :: [Int] -> Int -> Int -> Bool
canPlace [] _ _ = False
canPlace (x:xs) c d = go 1 x xs
  where
    go cnt _ [] = cnt >= c
    go cnt prev (y:ys)
      | y - prev >= d = go (cnt + 1) y ys
      | otherwise = go cnt prev ys