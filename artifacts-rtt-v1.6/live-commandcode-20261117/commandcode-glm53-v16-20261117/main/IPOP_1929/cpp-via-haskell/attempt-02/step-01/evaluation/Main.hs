module Main (main) where

import qualified Data.ByteString.Char8 as BS

main :: IO ()
main = do
  input <- BS.getContents
  let ws = BS.words input
  case ws of
    (a:b:_) ->
      let m = readInt a
          n = readInt b
          sieve = sieveUpTo n
          result = [i | i <- [m..n], sieve !! i]
      in mapM_ (\i -> BS.putStr (BS.pack (show i ++ "\n"))) result
    _ -> return ()
  where
    readInt s = maybe 0 fst (BS.readInt s)

sieveUpTo :: Int -> [Bool]
sieveUpTo n = go 2 (replicate (n+1) True)
  where
    go i arr
      | i * i > n = arr
      | arr !! i  = go (i+1) (mark i arr)
      | otherwise = go (i+1) arr
    mark i arr =
      [ if k >= i*i && k `mod` i == 0 then False else v
      | (k, v) <- zip [0..] arr ]