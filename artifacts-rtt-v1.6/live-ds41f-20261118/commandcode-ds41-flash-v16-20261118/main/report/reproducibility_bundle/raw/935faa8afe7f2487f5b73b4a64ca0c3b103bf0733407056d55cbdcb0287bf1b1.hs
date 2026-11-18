{-# LANGUAGE BangPatterns #-}

module Main where

import qualified Data.ByteString.Char8 as BS
import Data.List (sort)
import Data.Maybe (fromJust)

main :: IO ()
main = do
  input <- BS.getContents
  let toks = BS.words input
      nums = map (fst . fromJust . BS.readInt) toks
  case nums of
    (n : c : rest) -> do
      let houses = sort (take n rest)
      print (solve c houses)
    _ -> return ()

solve :: Int -> [Int] -> Int
solve c houses =
  let lo0 = 1
      hi0 = last houses - head houses
  in search lo0 hi0 0
  where
    search :: Int -> Int -> Int -> Int
    search !lo !hi !ans
      | lo > hi = ans
      | otherwise =
          let mid = lo + (hi - lo) `div` 2
          in if canPlace mid >= c
               then search (mid + 1) hi mid
               else search lo (mid - 1) ans

canPlace :: Int -> [Int] -> Int
canPlace d xs =
  case xs of
    [] -> 0
    (x : rest) -> go 1 x rest
  where
    go :: Int -> Int -> [Int] -> Int
    go !cnt !_ [] = cnt
    go !cnt !prev (y : ys)
      | y - prev >= d = go (cnt + 1) y ys
      | otherwise = go cnt prev ys