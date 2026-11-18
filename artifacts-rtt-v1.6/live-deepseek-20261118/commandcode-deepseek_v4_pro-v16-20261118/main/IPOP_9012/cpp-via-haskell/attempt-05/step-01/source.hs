module Main where

isValid :: String -> Bool
isValid = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs) =
      case c of
        '(' -> go (bal + 1) cs
        ')' | bal > 0 -> go (bal - 1) cs
            | otherwise -> False
        _ -> False

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    (tStr:rest) -> case reads tStr of
      [(t, "")] -> mapM_ (putStrLn . check) (take t rest)
      _ -> return ()
    _ -> return ()
  where
    check s = if isValid s then "YES" else "NO"