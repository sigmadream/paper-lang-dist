module Main where

valid :: String -> Bool
valid = go 0
  where
    go balance [] = balance == 0
    go balance (c:cs)
      | c == '('  = go (balance + 1) cs
      | balance == 0 = False
      | otherwise = go (balance - 1) cs

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (t:rest) ->
      let n = read t :: Int
      in mapM_ putStrLn [if valid s then "YES" else "NO" | s <- take n rest]