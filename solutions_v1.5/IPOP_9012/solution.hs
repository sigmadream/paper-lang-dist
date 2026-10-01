isValid :: String -> Bool
isValid = check 0
  where
    check depth _ | depth < 0 = False
    check depth [] = depth == 0
    check depth ('(':cs) = check (depth + 1) cs
    check depth (')':cs) = check (depth - 1) cs
    check depth (_:cs) = check depth cs

main :: IO ()
main = do
    content <- getContents
    case words content of
        [] -> return ()
        (_:cases) -> mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) cases
