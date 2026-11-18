module Main where

valid :: String -> Bool
valid = go 0
  where
    go balance [] = balance == 0
    go balance (c:cs)
      | c == '(' = go (balance + 1) cs
      | c == ')' = if balance == 0 then False else go (balance - 1) cs
      | otherwise = False

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (tStr : rest) -> do
      let t = read tStr :: Int
          strings = take t rest
      mapM_ output strings
  where
    output s = putStrLn (if valid s then "YES" else "NO")