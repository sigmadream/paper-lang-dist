module Main (main) where

import Data.IORef
import Data.Array
import System.IO

solve :: Int -> Int -> IORef Int -> IOUArray Int Bool -> IOUArray Int Bool -> IOUArray Int Bool -> IO ()
solve r n ans col diag1 diag2 =
  if r == n
    then modifyIORef' ans (+1)
    else mapM_ try [0 .. n - 1]
  where
    try c = do
      let d1 = r + c
          d2 = r - c + n - 1
      cUsed <- readArray col c
      d1Used <- readArray diag1 d1
      d2Used <- readArray diag2 d2
      if cUsed || d1Used || d2Used
        then return ()
        else do
          writeArray col c True
          writeArray diag1 d1 True
          writeArray diag2 d2 True
          solve (r + 1) n ans col diag1 diag2
          writeArray col c False
          writeArray diag1 d1 False
          writeArray diag2 d2 False

main :: IO ()
main = do
  inp <- getContents
  case map reads (lines inp) of
    ((n, _):_) | n >= 1 && n < 15 -> do
      ans <- newIORef 0
      col <- newListArray (0, n - 1) (replicate n False) :: IO (IOUArray Int Bool)
      diag1 <- newListArray (0, 2 * n - 2) (replicate (2 * n - 1) False) :: IO (IOUArray Int Bool)
      diag2 <- newListArray (0, 2 * n - 2) (replicate (2 * n - 1) False) :: IO (IOUArray Int Bool)
      solve 0 n ans col diag1 diag2
      result <- readIORef ans
      putStrLn (show result)
    _ -> return ()