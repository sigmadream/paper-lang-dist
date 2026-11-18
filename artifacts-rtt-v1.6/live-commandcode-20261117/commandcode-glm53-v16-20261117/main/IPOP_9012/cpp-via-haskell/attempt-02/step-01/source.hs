module Main (main) where

import Data.IORef

main :: IO ()
main = do
  first <- getLine
  case reads first of
    [(t, _)] -> mapM_ handle [1 .. t :: Int]
    _ -> return ()
  where
    handle _ = do
      l <- getLine
      putStrLn (if valid l then "YES" else "NO")
    bal :: String -> IORef Int -> IO Bool
    bal [] _ = return True
    bal (c:cs) r = do
      v <- readIORef r
      let v' = if c == '(' then v + 1 else v - 1
      if v' < 0
        then return False
        else do writeIORef r v'; bal cs r
    valid s = unsafeRun s
    unsafeRun s = let (ok, b) = go 0 s in ok && b == 0
      where
        go b [] = (True, b)
        go b (x:xs)
          | b' < 0 = (False, b')
          | otherwise = go b' xs
          where b' = if x == '(' then b + 1 else b - 1