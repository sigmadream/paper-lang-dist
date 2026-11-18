module Main where

isBalanced :: String -> Bool
isBalanced = go 0
  where
    go :: Int -> String -> Bool
    go n [] = n == 0
    go n ('(':xs) = go (n + 1) xs
    go 0 (')':_)  = False
    go n (')':xs) = go (n - 1) xs
    go _ _        = False   -- in case of unexpected character, treat as unbalanced

main :: IO ()
main = do
    input <- getContents
    let tokens = words input
    case tokens of
        (tStr:rest) -> do
            let t = read tStr :: Int
                strs = take t rest
            mapM_ (\s -> putStrLn $ if isBalanced s then "YES" else "NO") strs
        _ -> return ()