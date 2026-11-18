module Main where

check :: String -> Bool
check s = go 0 s
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '('  = go (bal + 1) cs
      | bal <= 0  = False
      | otherwise = go (bal - 1) cs

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (tStr:rest) -> do
      let t = read tStr :: Int
      mapM_ (putStrLn . boolToString . check) (take t rest)
  where
    boolToString True  = "YES"
    boolToString False = "NO"