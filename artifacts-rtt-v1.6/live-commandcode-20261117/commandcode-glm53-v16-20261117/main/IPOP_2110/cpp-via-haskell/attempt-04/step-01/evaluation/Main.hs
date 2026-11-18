module Main (main) where

import Data.List (sort)
import qualified Data.ByteString.Char8 as BS

main :: IO ()
main = do
  input <- BS.getContents
  let (n : c : rest) = map (maybe 0 fst . BS.readInt) (BS.words input)
      xs = map (maybe 0 fst . BS.readInt) rest
      a = sort xs
      lo = head a
      hi = last a
      go l r ans
        | l > r = ans
        | otherwise =
            let mid = l + (r - l) `div` 2
                cnt = countInstalled mid
                countInstalled m = 1 + goCount (tail a) (head a) m
                goCount [] _ _ = 0
                goCount (y:ys) p m
                  | y - p >= m = 1 + goCount ys y m
                  | otherwise = goCount ys p m
            in if cnt >= c
                 then go (mid + 1) r mid
                 else go l (mid - 1) ans
  print (go 1 (hi - lo) 0)