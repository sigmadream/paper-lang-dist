main :: IO ()
main = do
    s <- getLine
    if s == reverse s then putStrLn "1" else putStrLn "0"