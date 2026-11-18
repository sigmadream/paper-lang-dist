module Main where

isValid :: String -> Bool
isValid s = go 0 s
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '(' = go (bal + 1) cs
      | c == ')' = if bal == 0 then False else go (bal - 1) cs
      | otherwise = False

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> pure ()
    (tStr : rest) ->
      case reads tStr :: [(Int, String)] of
        [(t, "")] -> mapM_ (putStrLn . \s -> if isValid s then "YES" else "NO") (take t rest)
        _ -> pure ()