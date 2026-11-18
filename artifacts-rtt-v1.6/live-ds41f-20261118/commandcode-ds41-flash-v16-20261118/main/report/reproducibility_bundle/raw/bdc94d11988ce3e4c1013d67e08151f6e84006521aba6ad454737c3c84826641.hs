module Main where

check :: String -> String
check s = go 0 s
  where
    go balance [] =
      if balance == 0 then "YES" else "NO"
    go balance ('(' : xs) = go (balance + 1) xs
    go balance (')' : xs)
      | balance == 0 = "NO"
      | otherwise = go (balance - 1) xs
    go balance (_ : xs) = go balance xs

main :: IO ()
main = do
  input <- getContents
  let tokens = words input
  case tokens of
    [] -> return ()
    (t : rest) -> do
      let n = read t :: Int
          strings = take n rest
      mapM_ (putStrLn . check) strings