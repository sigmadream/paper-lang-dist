module Main where

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (t:rest) -> do
      let n = read t :: Int
          ans = map (\s -> if valid s then "YES" else "NO") (take n rest)
      putStr (unlines ans)

valid :: String -> Bool
valid = go 0
  where
    go b [] = b == 0
    go b ('(':xs) = go (b + 1) xs
    go b (')':xs) = b > 0 && go (b - 1) xs
    go _ _ = False