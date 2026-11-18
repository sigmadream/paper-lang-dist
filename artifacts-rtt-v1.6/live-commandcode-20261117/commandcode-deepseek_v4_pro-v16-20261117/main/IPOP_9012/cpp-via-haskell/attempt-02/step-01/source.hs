module Main where

import Control.Monad (mapM_)

isValid :: String -> Bool
isValid s = go 0 s
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
        [] -> return ()
        (tStr:rest) -> do
            let t = read tStr :: Int
                strs = take t rest
            mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) strs