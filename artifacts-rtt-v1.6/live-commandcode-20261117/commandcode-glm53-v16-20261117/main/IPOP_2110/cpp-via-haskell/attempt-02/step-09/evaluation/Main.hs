module Main (main) where

import qualified Data.Vector.Unboxed as V
import qualified Data.Vector.Unboxed.Mutable as VM
import qualified Data.Vector.Algorithms.Intro as VI
import Data.Vector.Unboxed ((!))
import Control.Monad

main :: IO ()
main = do
  first <- getLine
  let (nStr:cStr:_) = words first
      n = read nStr :: Int
      c = read cStr :: Integer
  mv <- VM.new n
  forM_ [0..n-1] $ \i -> do
    l <- getLine
    VM.write mv i (read l :: Integer)
  v <- V.unsafeFreeze mv
  let s = V.modify VI.sort v
      lo0 = 1
      hi0 = s ! (n-1) - s ! 0
      feasible mid = go 1 (s ! 0) 1
        where
          go i p k
            | i >= n = k
            | s ! i - p >= mid = go (i+1) (s ! i) (k+1)
            | otherwise = go (i+1) p k
      search lo hi ans
        | lo > hi = ans
        | feasible mid >= c = search (mid+1) hi mid
        | otherwise = search lo (mid-1) ans
        where mid = lo + (hi - lo) `div` 2
  print (search lo0 hi0 0)