module Main where

check :: String -> Bool
check = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '(' = go (bal + 1) cs
      | bal <= 0 = False
      | otherwise = go (bal - 1) cs

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> pure ()
    (tStr:rest) -> do
      let t = read tStr :: Int
          results = map check (take t rest)
      putStr (unlines [if ok then "YES" else "NO" | ok <- results])