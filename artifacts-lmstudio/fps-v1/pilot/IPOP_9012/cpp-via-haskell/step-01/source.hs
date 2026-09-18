main :: IO ()
main = do
    t <- readLn :: IO Int
    replicateM_ t $ do
        s <- getLine
        let bal = foldl (\acc c -> if c == '(' then acc + 1 else acc - 1) 0 s
        putStrLn $ if bal == 0 && all (`elem` "()") s then "YES" else "NO"