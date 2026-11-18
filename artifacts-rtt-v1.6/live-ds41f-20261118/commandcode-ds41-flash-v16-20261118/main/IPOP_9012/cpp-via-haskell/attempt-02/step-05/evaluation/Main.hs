module Main where

valid :: String -> Bool
valid = go 0
  where
    go balance [] = balance == 0
    go balance (c:cs)
      | c == '(' = go (balance + 1) cs
      | balance == 0 = False
      | otherwise = go (balance - 1) cs

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (tStr:rest) -> do
      let t = read tStr :: Int
          strings = take t rest
          output = [if valid s then "YES" else "NO" | s <- strings]
      putStr (unlines output)