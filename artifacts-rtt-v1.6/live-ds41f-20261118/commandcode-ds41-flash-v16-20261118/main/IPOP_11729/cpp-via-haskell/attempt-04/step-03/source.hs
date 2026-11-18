import qualified Data.ByteString.Builder as B
import Data.Bits (shiftL)
import System.IO (stdout)

hanoiB :: Int -> Int -> Int -> Int -> B.Builder
hanoiB 0 _ _ _ = mempty
hanoiB 1 a _ c = B.intDec a <> B.charUtf8 ' ' <> B.intDec c <> B.charUtf8 '\n'
hanoiB n a b c = hanoiB (n - 1) a c b <> hanoiB 1 a b c <> hanoiB (n - 1) b a c

main :: IO ()
main = do
  input <- getContents
  case words input of
    (x:_) -> do
      let n = read x :: Int
      let cnt = (1 `shiftL` n) - 1
      let out = B.intDec cnt <> B.charUtf8 '\n' <> hanoiB n 1 2 3
      B.hPutBuilder stdout out
    [] -> return ()