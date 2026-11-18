module Main where

main :: IO ()
main = do
    input <- getContents
    let ws = words input
    if null ws
        then return ()
        else do
            let t = read (head ws) :: Int
                strs = take t (tail ws)
            mapM_ (putStrLn . check) strs

check :: String -> String
check s = if valid s then "YES" else "NO"

valid :: String -> Bool
valid = go 0
  where
    go :: Int -> String -> Bool
    go bal [] = bal == 0
    go bal (c:cs) =
        let bal' = if c == '(' then bal + 1 else bal - 1
        in bal' >= 0 && go bal' cs