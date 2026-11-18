module Main where

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (t:rest) ->
      mapM_ putStrLn (map (answer . check) (take (read t) rest))

check :: String -> Bool
check = go 0
  where
    go bal [] = bal == 0
    go bal (c:cs)
      | c == '(' = go (bal + 1) cs
      | bal <= 0 = False
      | otherwise = go (bal - 1) cs

answer :: Bool -> String
answer True = "YES"
answer False = "NO"