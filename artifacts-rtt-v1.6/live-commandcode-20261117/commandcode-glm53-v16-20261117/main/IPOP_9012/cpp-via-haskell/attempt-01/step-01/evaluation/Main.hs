module Main (main) where

import Data.IORef

main :: IO ()
main = do
  inp <- getContents
  case lines inp of
    [] -> return ()
    (tLine:rest) -> mapM_ (putStrLn . check) (take (read tLine :: Int) rest)
  where
    check s
      | go 0 s = "YES"
      | otherwise = "NO"
    go _ [] = True
    go bal (c:cs)
      | bal < 0 = False
      | c == '(' = go (bal + 1) cs
      | otherwise = go (bal - 1) cs