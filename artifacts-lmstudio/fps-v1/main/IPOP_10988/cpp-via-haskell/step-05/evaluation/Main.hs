main :: IO ()
main = do
    input <- getLine
    let reversedInput = reverse input
    if input == reversedInput then putStrLn "1" else putStrLn "0"