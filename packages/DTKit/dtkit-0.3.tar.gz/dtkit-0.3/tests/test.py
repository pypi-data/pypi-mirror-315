import unittest
from dtkit import Temperature, Color

class TestTemperature(unittest.TestCase):
    def test_initialization(self):
        t = Temperature(25, "C")
        self.assertEqual(t.value, 25)
        self.assertEqual(t.unit, "C")

        with self.assertRaises(ValueError):
            Temperature(100, "X")

    def test_conversion(self):
        t = Temperature(0, "C")
        self.assertAlmostEqual(t.to_fahrenheit(), 32)
        self.assertAlmostEqual(t.to_kelvin(), 273.15)

        t = Temperature(32, "F")
        self.assertAlmostEqual(t.to_celsius(), 0)
        self.assertAlmostEqual(t.to_kelvin(), 273.15)

        t = Temperature(273.15, "K")
        self.assertAlmostEqual(t.to_celsius(), 0)
        self.assertAlmostEqual(t.to_fahrenheit(), 32)

    def test_is_freezing(self):
        t = Temperature(0, "C")
        self.assertTrue(t.is_freezing())

        t = Temperature(32, "F")
        self.assertTrue(t.is_freezing())

        t = Temperature(100, "C")
        self.assertFalse(t.is_freezing())

    def test_is_boiling(self):
        t = Temperature(100, "C")
        self.assertTrue(t.is_boiling())

        t = Temperature(212, "F")
        self.assertTrue(t.is_boiling())

        t = Temperature(50, "C")
        self.assertFalse(t.is_boiling())

    def test_arithmetic(self):
        t1 = Temperature(25, "C")
        t2 = Temperature(77, "F")  # Equivalent to 25°C

        result_add = t1 + t2
        self.assertEqual(result_add.value, 50)
        self.assertEqual(result_add.unit, "C")

        result_sub = t1 - t2
        self.assertEqual(result_sub.value, 0)
        self.assertEqual(result_sub.unit, "C")


class TestColor(unittest.TestCase):
    def test_initialization(self):
        c = Color(255, 0, 0)
        self.assertEqual(c.red, 255)
        self.assertEqual(c.green, 0)
        self.assertEqual(c.blue, 0)

        with self.assertRaises(ValueError):
            Color(300, 0, 0)

    def test_to_hex(self):
        c = Color(255, 0, 0)
        self.assertEqual(c.to_hex(), "#FF0000")

        c = Color(0, 255, 0)
        self.assertEqual(c.to_hex(), "#00FF00")

        c = Color(0, 0, 255)
        self.assertEqual(c.to_hex(), "#0000FF")

    def test_from_hex(self):
        c = Color.from_hex("#FF0000")
        self.assertEqual(c.red, 255)
        self.assertEqual(c.green, 0)
        self.assertEqual(c.blue, 0)

        with self.assertRaises(ValueError):
            Color.from_hex("#XYZ123")

    def test_to_hsl(self):
        c = Color(255, 0, 0)
        self.assertEqual(c.to_hsl(), (0.0, 100.0, 50.0))

        c = Color(0, 255, 0)
        self.assertEqual(c.to_hsl(), (120.0, 100.0, 50.0))

        c = Color(0, 0, 255)
        self.assertEqual(c.to_hsl(), (240.0, 100.0, 50.0))

    def test_range(self):
        start = Color(255, 0, 0)
        end = Color(0, 0, 255)
        gradient = Color.range(start, end, 3)
        self.assertEqual(gradient[0].to_hex(), "#FF0000")
        self.assertEqual(gradient[1].to_hex(), "#800080")
        self.assertEqual(gradient[2].to_hex(), "#0000FF")

    def test_blend(self):
        c1 = Color(255, 0, 0)
        c2 = Color(0, 0, 255)
        blended = c1.blend(c2, ratio=0.5)
        self.assertEqual(blended.to_hex(), "#800080")

    def test_invert(self):
        c = Color(255, 255, 255)
        self.assertEqual(c.invert().to_hex(), "#000000")

        c = Color(0, 0, 0)
        self.assertEqual(c.invert().to_hex(), "#FFFFFF")

    def test_brightness(self):
        c = Color(255, 0, 0)  # Bright red
        self.assertEqual(c.brightness(), 76.24)

        c = Color(0, 0, 0)  # Black
        self.assertEqual(c.brightness(), 0.0)

        c = Color(255, 255, 255)  # White
        self.assertEqual(c.brightness(), 255.0)


if __name__ == "__main__":
    unittest.main()
