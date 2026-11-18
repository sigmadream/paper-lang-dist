module Main where

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (tStr : rest) -> do
      let t = read tStr :: Int
          cases = take t rest
      putStr (unlines (map check cases))

check :: String -> String
check s = go s 0
  where
    go [] balance = if balance == 0 then "YES" else "NO"
    go (c : cs) balance
      | c == '(' = go cs (balance + 1)
      | c == ')' =
          if balance == 0
            then "NO"
            else go cs (balance - 1)
      | otherwise = go cs balance