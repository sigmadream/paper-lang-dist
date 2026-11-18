module Main where

import Control.Monad (forM_)

isBalanced :: String -> Bool
isBalanced = check 0
  where
    check bal [] = bal == 0
    check bal (c:cs)
      | c == '(' = check (bal + 1) cs
      | c == ')' = if bal > 0 then check (bal - 1) cs else False
      | otherwise = False

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    (tStr : rest) -> do
      let t = read tStr :: Int
      forM_ (take t rest) $ \s ->
        putStrLn (if isBalanced s then "YES" else "NO")
    _ -> return ()