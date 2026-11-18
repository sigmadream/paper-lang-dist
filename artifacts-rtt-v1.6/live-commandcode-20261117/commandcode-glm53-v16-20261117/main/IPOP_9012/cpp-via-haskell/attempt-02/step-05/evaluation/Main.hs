module Main (main) where

import System.IO

main :: IO ()
main = do
  contents <- getContents
  let ls = lines contents
  case ls of
    (tStr:rest) -> mapM_ (putStrLn . judge) (take (read tStr :: Int) rest)
    _ -> return ()
  where
    judge s = if check 0 s then "YES" else "NO"
    check b [] = b == 0
    check b (c:cs)
      | b' < 0 = False
      | otherwise = check b' cs
      where b' = if c == '(' then b + 1 else b - 1