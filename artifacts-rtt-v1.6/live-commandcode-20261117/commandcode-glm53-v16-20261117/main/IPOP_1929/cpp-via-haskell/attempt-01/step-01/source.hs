module Main (main) where

import qualified Data.ByteString as BS
import qualified Data.ByteString.Char8 as BC
import Data.Maybe (fromMaybe)

main :: IO ()
main = do
  inp <- BS.getContents
  let ws = BC.words inp
      (m, n) = case ws of
        (x:y:_) -> (maybe 1 fst (BC.readInt x), maybe 1 fst (BC.readInt y))
        _ -> (1, 1)
      sieve = BC.pack [ if p then '1' else '0' | p <- mkSieve n ]
      mkSieve lim = go 2 (replicate (lim + 1) True)
        where
          go i arr
            | i * i > lim = arr
            | arr !! i = go (i + 1) (mark i arr)
            | otherwise = go (i + 1) arr
          mark i arr = [ if k >= i * i && (k - i * i) `mod` i == 0 then False else a
                       | (k, a) <- zip [0..] arr ]
      isPrime k = sieve `BC.index` k == '1'
      out = BC.unlines [ BC.pack (show k) | k <- [m..n], isPrime k ]
  BC.putStr out