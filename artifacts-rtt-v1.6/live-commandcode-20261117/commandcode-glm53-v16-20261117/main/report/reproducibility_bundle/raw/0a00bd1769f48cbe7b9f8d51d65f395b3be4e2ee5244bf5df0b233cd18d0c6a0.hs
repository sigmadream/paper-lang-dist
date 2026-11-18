module Main (main) where

import Data.List (sort)
import qualified Data.ByteString.Char8 as BS

main :: IO ()
main = do
  input <- BS.getContents
  let nums = map (maybe 0 id . readInt) (BS.words input)
      (n : c : rest) = nums
      a = sort (take n rest)
  print (solve a c)

readInt :: BS.ByteString -> Maybe Int
readInt s = case BS.readInt s of
  Just (v, _) -> Just v
  Nothing -> Nothing

solve :: [Int] -> Int -> Int
solve a c = go 1 (last a - head a) 0
  where
    go l r ans
      | l > r = ans
      | otherwise =
          let mid = l + (r - l) `div` 2
              cnt = countGE mid
          in if cnt >= c
               then go (mid + 1) r mid
               else go l (mid - 1) ans
    countGE mid = walk a
      where
        walk (x:xs) = walkFrom x 1 xs
        walk [] = 0
        walkFrom prev k (x:xs)
          | x - prev >= mid = walkFrom x (k+1) xs
          | otherwise = walkFrom prev k xs
        walkFrom _ k [] = k