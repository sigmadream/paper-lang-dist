module Main where

isValid :: String -> Bool
isValid = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '('  = go (bal + 1) cs
      | c == ')'  = bal > 0 && go (bal - 1) cs
      | otherwise = False

main :: IO ()
main = do
    input <- getContents
    let (tLine:strLines) = lines input
        t = read tLine :: Int
        ss = take t strLines
    mapM_ (\s -> putStrLn (if isValid s then "YES" else "NO")) ss