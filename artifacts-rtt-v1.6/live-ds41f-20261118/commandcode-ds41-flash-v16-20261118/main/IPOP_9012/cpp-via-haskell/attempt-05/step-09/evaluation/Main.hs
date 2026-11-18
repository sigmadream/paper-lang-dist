module Main where

isValid :: String -> Bool
isValid = go 0
  where
    go balance [] = balance == 0
    go balance (c:cs)
      | c == '(' = go (balance + 1) cs
      | c == ')' = if balance == 0 then False else go (balance - 1) cs
      | otherwise = False

main :: IO ()
main = do
  input <- getContents
  case lines input of
    [] -> return ()
    (tLine:rest) -> do
      let t = read tLine :: Int
      mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) (take t rest)