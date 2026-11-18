module Main (main) where

import Data.IORef

main :: IO ()
main = do
  n <- readLn :: IO Int
  ref <- newIORef []
  let hanoi 1 s _ e = modifyIORef' ref ((s, e) :)
      hanoi k s m e = do
        hanoi (k - 1) s e m
        modifyIORef' ref ((s, e) :)
        hanoi (k - 1) m s e
  hanoi n 1 2 3
  moves <- reverse <$> readIORef ref
  print (length moves)
  mapM_ (\(a, b) -> putStrLn (show a ++ " " ++ show b)) moves