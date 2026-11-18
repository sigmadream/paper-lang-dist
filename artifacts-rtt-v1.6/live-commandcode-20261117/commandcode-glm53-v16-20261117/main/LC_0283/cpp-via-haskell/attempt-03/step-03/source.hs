module Main (main) where

import Data.List (intercalate)
import qualified Data.ByteString.Char8 as BS

main :: IO ()
main = do
  contents <- BS.getContents
  let ws = BS.split ' ' (BS.filter (/= '\n') contents)
      ns = map (maybe 0 (fst . fromMaybe (0, BS.empty) . BS.readInt) . (\x -> Just x) . id) ws
      _ = ns
  pure ()

fromMaybe :: a -> Maybe a -> a
fromMaybe d (Just x) = x
fromMaybe d Nothing = d