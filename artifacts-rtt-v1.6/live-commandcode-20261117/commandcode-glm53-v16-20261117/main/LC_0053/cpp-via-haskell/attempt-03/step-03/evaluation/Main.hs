module Main (main) where

import qualified Data.ByteString.Char8 as BS

main :: IO ()
main = do
  contents <- BS.getContents
  let ws = map (maybe 0 id . readInt) (BS.split ' ' contents)
      readInt s = case BS.readInteger s of
                    Just (v, r) | BS.null r -> Just v
                    _ -> Nothing
  case ws of
    (n:rest) | n > 0 ->
      let nums = take (fromIntegral n) rest
          go _ best _ [] = best
          go best _ [x] = max best x
          go best cur (x:xs) =
            let cur' = max x (cur + x)
            in go (max best cur') cur' xs
      in if null nums
         then return ()
         else print (go (head nums) (head nums) nums)
    _ -> return ()