module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (t:_) ->
            let n = read t :: Int
                strings = take n (tail tokens)
            in mapM_ (putStrLn . check) strings

check :: String -> String
check s = go s 0
  where
    go [] 0 = "YES"
    go [] _ = "NO"
    go ('(':xs) n = go xs (n + 1)
    go (')':xs) n
        | n <= 0 = "NO"
        | otherwise = go xs (n - 1)
    go (_:xs) n = go xs n