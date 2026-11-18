module Main where

import Control.Monad (when, forM_)
import Data.Array.ST (runSTUArray)
import Data.Array.MArray (newArray, readArray, writeArray)
import Data.Array.Unboxed (UArray, (!))

solve :: Int -> Int -> [Int]
solve m n = [i | i <- [m..n], arr ! i == 1]
  where
    arr :: UArray Int Int
    arr = runSTUArray $ do
      a <- newArray (0, n) (1 :: Int)
      when (n >= 0) $ writeArray a 0 0
      when (n >= 1) $ writeArray a 1 0
      let limit = floor (sqrt (fromIntegral n)) :: Int
      forM_ [2 .. limit] $ \i -> do
        p <- readArray a i
        when (p == 1) $
          forM_ [i * i, i * i + i .. n] $ \j ->
            writeArray a j 0
      return a

main :: IO ()
main = do
  input <- getContents
  let nums = map read (words input) :: [Int]
  case nums of
    (m:n:_) -> putStr $ concatMap (\x -> show x ++ "\n") (solve m n)
    _ -> return ()