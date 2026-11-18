module Main where

isValid :: String -> Bool
isValid = go 0
  where
    go :: Int -> String -> Bool
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '(' = go (bal + 1) cs
      | c == ')' = bal > 0 && go (bal - 1) cs
      | otherwise = go bal cs

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
      [] -> return ()
      (tStr:rest) -> do
        let t = read tStr :: Int
        mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) (take t rest)