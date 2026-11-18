module Main where

valid :: String -> Bool
valid = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '(' = go (bal + 1) cs
      | otherwise = bal > 0 && go (bal - 1) cs

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (t:_) ->
      let n = read t :: Int
          strings = take n (drop 1 ws)
      in mapM_ (putStrLn . check) strings
  where
    check s = if valid s then "YES" else "NO"