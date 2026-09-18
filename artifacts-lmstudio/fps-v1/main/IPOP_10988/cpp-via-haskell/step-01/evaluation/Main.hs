main :: IO ()
main = do
    input <- getLine
    let result = if input == reverse input then "1" else "0"
    putStrLn result