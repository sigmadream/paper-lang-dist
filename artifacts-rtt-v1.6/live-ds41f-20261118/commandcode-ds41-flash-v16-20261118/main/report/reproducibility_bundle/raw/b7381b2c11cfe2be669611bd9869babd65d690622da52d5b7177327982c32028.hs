module Main where

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        [] -> return ()
        (tStr:rest) -> do
            let t = read tStr :: Int
                strings = take t rest
            putStr $ unlines $ map (answer . isValid) strings

isValid :: String -> Bool
isValid s = go s 0
  where
    go [] balance = balance == 0
    go (c:cs) balance
        | c == '(' = go cs (balance + 1)
        | c == ')' = balance > 0 && go cs (balance - 1)
        | otherwise = False

answer :: Bool -> String
answer True = "YES"
answer False = "NO"