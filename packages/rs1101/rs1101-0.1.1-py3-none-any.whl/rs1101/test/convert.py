import unittest
import rs1101.random_string as rs
from secrets import randbelow


class TestConvertMethods(unittest.TestCase):
    def test_convert(self):
        for _ in range(100):
            s = rs.random_string(randbelow(30))
            l = len(s)
            x = rs.rs2int(s)
            y = rs.int2rs(x, l)
            try:
                assert s == y
            except Exception as e:
                print(e, s, x, y)

    def test_convert_example(self):
        s = "AHCJVUj3l"
        x = rs.rs2int(s)
        y = rs.int2rs(x)
        try:
            assert s[1:] == y
            assert isinstance(s, str)
            assert s == rs.int2rs(x, len(s))
        except Exception as e:
            print(e, s, x, y)


if __name__ == "__main__":
    unittest.main()
