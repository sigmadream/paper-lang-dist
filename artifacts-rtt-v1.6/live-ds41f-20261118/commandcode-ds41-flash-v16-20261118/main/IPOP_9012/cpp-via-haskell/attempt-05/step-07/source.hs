module Main where

isValid :: String -> Bool
isValid s = go 0 s
  where
    go balance [] = balance == 0
    go balance (c:cs)
      | c == '(' = go (balance + 1) cs
      | c == ')' = if balance == 0 then False else go (balance - 1) cs
      | otherwise = False

main :: IO ()
main = do
  input <- getContents
  let ls = lines input
  case ls of
    [] -> return ()
    (tLine:rest) -> do
      let t = read tLine :: Int
          strings = take t rest
      mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) strings