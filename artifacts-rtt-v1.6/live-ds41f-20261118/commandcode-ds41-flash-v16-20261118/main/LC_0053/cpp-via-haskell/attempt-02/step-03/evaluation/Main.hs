module Main where

import Data.List (foldl')
import Text.Read (readMaybe)

takeParsed :: Int -> [String] -> [Integer]
takeParsed k _ | k <= 0 = []
takeParsed _ [] = []
takeParsed k (s:ss) =
  case readMaybe s :: Maybe Integer of
    Nothing -> []
    Just x  -> x : takeParsed (k - 1) ss

main :: IO ()
main = do
  input <- getContents
  let ws = words input
  case ws of
    [] -> return ()
    (nw : rest) ->
      case readMaybe nw :: Maybe Integer of
        Nothing -> return ()
        Just n -> do
          let k = if n <= 0 then 0 else fromInteger n
              nums = takeParsed k rest
          case nums of
            [] -> putStrLn "0"
            (x:xs) -> do
              let step (cur, best) v =
                    let cur' = max v (cur + v)
                        best' = max best cur'
                    in (cur', best')
                  (_, ans) = foldl' step (x, x) xs
              print ans