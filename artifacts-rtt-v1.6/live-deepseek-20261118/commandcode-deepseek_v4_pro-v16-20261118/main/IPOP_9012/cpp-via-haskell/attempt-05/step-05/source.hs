module Main where

isValid :: String -> Bool
isValid = go 0
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
        [] -> return ()
        (tStr : rest) ->
            let t = read tStr :: Int
                strings = take t rest
            in mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) strings