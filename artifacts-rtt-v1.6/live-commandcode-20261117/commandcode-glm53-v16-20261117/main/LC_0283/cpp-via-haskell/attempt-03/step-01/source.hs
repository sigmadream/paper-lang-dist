module Main (main) where

import Data.List (intercalate)
import qualified Data.ByteString.Char8 as BS

main :: IO ()
main = do
  _ <- readLine
  rest <- BS.getContents
  let nums = map (fst . fromJust' . BS.readInteger) (BS.words rest)
      nonZeros = filter (/= 0) nums
      zeros = filter (== 0) nums
      result = nonZeros ++ zeros
  putStrLn (intercalate " " (map show result))
  where
    fromJust' (Just x) = x
    fromJust' Nothing  = error "bad input"

readLine :: IO BS.ByteString
readLine = BS.getLine