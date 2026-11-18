module Main where

import Control.Monad (forM_)
import Text.Read (readMaybe)

isBalanced :: String -> Bool
isBalanced = go 0
  where
    go bal [] = bal == 0
    go bal ('(':xs) = go (bal + 1) xs
    go bal (')':xs)
      | bal > 0 = go (bal - 1) xs
      | otherwise = False
    go _ _ = False

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    (tStr:rest) ->
      case readMaybe tStr :: Maybe Int of
        Just t ->
          mapM_ putStrLn
            [ if isBalanced s then "YES" else "NO"
            | s <- take t rest
            ]
        Nothing -> return ()
    [] -> return ()