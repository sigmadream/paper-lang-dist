module Main (main) where

import Data.IORef
import qualified Data.IntSet as Set
import System.IO

solve :: Int -> IORef Int -> Int -> Int -> Int -> Int -> Int -> IO ()
solve n ans r cols d1 d2
  | r == n = modifyIORef' ans (+1)
  | otherwise = go 0
  where
    go c
      | c == n = return ()
      | otherwise = do
          let a = r + c
              b = r - c + n - 1
          if c `Set.member` cols || a `Set.member` d1 || b `Set.member` d2
            then go (c + 1)
            else do
              solve n ans (r + 1) (Set.insert c cols) (Set.insert a d1) (Set.insert b d2)
              go (c + 1)

main :: IO ()
main = do
    inp <- getContents
    case words inp of
        (s:_) -> do
            let n = read s :: Int
            ans <- newIORef (0 :: Int)
            solve n ans 0 Set.empty Set.empty Set.empty
            r <- readIORef ans
            print r
        [] -> return ()