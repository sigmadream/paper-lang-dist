main :: IO ()
main = do
    n <- readLn :: IO Int
    strings <- replicateM n getLine
    mapM_ (putStrLn . checkBalance) strings

checkBalance :: String -> String
checkBalance s = if isBalanced s then "YES" else "NO"

isBalanced :: String -> Bool
isBalanced = go 0
  where
    go depth [] = depth == 0
    go depth (c:cs)
        | c == '(' = go (depth + 1) cs
        | c == ')' = if depth > 0 then go (depth - 1) cs else False
        | otherwise = False