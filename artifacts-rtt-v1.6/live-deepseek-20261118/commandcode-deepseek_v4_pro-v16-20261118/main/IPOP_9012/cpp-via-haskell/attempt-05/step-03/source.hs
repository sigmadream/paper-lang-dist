module Main where

import Control.Monad (forM_)
import Text.Read (readMaybe)

isValid :: String -> Bool
isValid = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs)
        | c == '(' = go (bal + 1) cs
        | c == ')' = bal > 0 && go (bal - 1) cs
        | otherwise = False

main :: IO ()
main = do
    input <- getContents
    case words input of
        [] -> return ()
        (tStr : rest) ->
            case readMaybe tStr :: Maybe Int of
                Nothing -> return ()
                Just t ->
                    forM_ (take t rest) $ \s ->
                        putStrLn (if isValid s then "YES" else "NO")