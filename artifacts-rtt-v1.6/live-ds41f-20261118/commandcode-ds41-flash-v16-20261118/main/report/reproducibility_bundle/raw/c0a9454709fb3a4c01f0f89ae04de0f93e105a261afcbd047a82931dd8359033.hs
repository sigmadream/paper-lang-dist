module Main where

valid :: String -> Bool
valid s = go 0 s
  where
    go 0 [] = True
    go _ [] = False
    go balance ('(' : xs) = go (balance + 1) xs
    go 0 (')' : _) = False
    go balance (')' : xs) = go (balance - 1) xs
    go _ _ = False

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (tStr : rest) -> do
      let t = read tStr :: Int
      mapM_ (putStrLn . verdict) (take t rest)
  where
    verdict s = if valid s then "YES" else "NO"