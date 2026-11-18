module Main where

import Data.List (words)

isBalanced :: String -> Bool
isBalanced = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '(' = go (bal + 1) cs
      | c == ')' = if bal > 0 then go (bal - 1) cs else False
      | otherwise = False

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (tStr : rest) ->
      case reads tStr :: [(Int, String)] of
        [(t, "")] ->
          mapM_ (putStrLn . judge) (take t rest)
        _ -> return ()
  where
    judge s = if isBalanced s then "YES" else "NO"