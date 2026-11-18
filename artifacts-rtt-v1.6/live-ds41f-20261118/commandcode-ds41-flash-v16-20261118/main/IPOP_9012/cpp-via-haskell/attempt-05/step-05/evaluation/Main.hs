module Main where

isValid :: String -> Bool
isValid s = go 0 s
  where
    go 0 [] = True
    go _ [] = False
    go balance (c:cs)
      | c == '(' = go (balance + 1) cs
      | c == ')' = balance > 0 && go (balance - 1) cs
      | otherwise = False

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (tStr:rest) -> do
      let t = read tStr :: Int
          strings = take t rest
      mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) strings