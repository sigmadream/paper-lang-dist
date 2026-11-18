module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (t:rest) -> mapM_ (putStrLn . check) (take (read t) rest)

check :: String -> String
check s = if valid s then "YES" else "NO"

valid :: String -> Bool
valid = go 0
  where
    go 0 [] = True
    go _ [] = False
    go bal (c:cs)
        | c == '(' = go (bal + 1) cs
        | bal == 0 = False
        | otherwise = go (bal - 1) cs