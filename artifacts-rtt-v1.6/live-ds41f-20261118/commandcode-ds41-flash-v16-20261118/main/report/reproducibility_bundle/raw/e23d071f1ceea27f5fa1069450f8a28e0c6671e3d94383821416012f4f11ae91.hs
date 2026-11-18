module Main where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)
import Data.Char (isSpace)

parseInts :: BS.ByteString -> [Int]
parseInts bs =
  let s = BS.dropWhile isSpace bs
  in if BS.null s
       then []
       else case BS.readInt s of
              Just (x, rest) -> x : parseInts rest
              Nothing -> []

countPlacements :: Int -> [Int] -> Int
countPlacements d xs =
  case xs of
    [] -> 0
    (h:hs) -> go 1 h hs
  where
    go cnt _ [] = cnt
    go cnt prev (y:ys)
      | y - prev >= d = go (cnt + 1) y ys
      | otherwise     = go cnt prev ys

maxMinDistance :: [Int] -> Int -> Int
maxMinDistance homes c = search 1 (last homes - head homes) 0
  where
    search lo hi best
      | lo > hi = best
      | otherwise =
          let mid = lo + (hi - lo) `div` 2
          in if countPlacements mid homes >= c
               then search (mid + 1) hi mid
               else search lo (mid - 1) best

main :: IO ()
main = do
  input <- BS.getContents
  case parseInts input of
    (n:c:rest) -> do
      let homes = sort (take n rest)
      print (maxMinDistance homes c)
    _ -> return ()