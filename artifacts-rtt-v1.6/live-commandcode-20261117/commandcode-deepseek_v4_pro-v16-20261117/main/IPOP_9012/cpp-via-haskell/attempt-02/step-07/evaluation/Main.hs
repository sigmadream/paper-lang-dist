module Main where

isValid :: String -> Bool
isValid = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '(' = go (bal + 1) cs
      | c == ')' = bal > 0 && go (bal - 1) cs
      | otherwise = False

result :: String -> String
result s
  | isValid s = "YES"
  | otherwise = "NO"

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
      [] -> pure ()
      (tStr:rest) -> do
          let t = read tStr :: Int
          mapM_ (putStrLn . result) (take t rest)