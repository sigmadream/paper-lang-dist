module Main where

main :: IO ()
main = do
  input <- getContents
  case words input of
    [] -> return ()
    (t:rest) ->
      let count = read t :: Int
      in mapM_ (putStrLn . isValid) (take count rest)

isValid :: String -> String
isValid s =
  let balances = scanl (\bal c -> if c == '(' then bal + 1 else bal - 1) 0 s
  in if all (>= 0) balances && last balances == 0
       then "YES"
       else "NO"