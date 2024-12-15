import unittest
from java.lang import Object
from java.util import ArrayList
import jep

TestPyJObject = jep.findClass('jep.test.TestPyJObject')

class TestObject(unittest.TestCase):

    def test_hash(self):
        o = Object()
        self.assertTrue(isinstance(hash(o), int))

    def test_str(self):
        o = Object()
        self.assertIn('java.lang.Object@', str(o))

    def test_toString(self):
        o = Object()
        self.assertIn('java.lang.Object@', o.toString())

    def test_repr(self):
        self.assertEqual(repr(TestPyJObject.ReprClass()), "ReprClass")
        self.assertEqual(repr(TestPyJObject.ReprSubClass()), "ReprSubClass")
        self.assertIn("<java.lang.Object object at", repr(Object()))

    def test_add(self):
        self.assertEqual(TestPyJObject.AddClass() + 6, 7)

    def test_del_throws_exception(self):
        o = Object()
        with self.assertRaises(AttributeError):
            del o.equals
        with self.assertRaises(AttributeError):
            o.bad = 7
        # Subtypes can behave differently then base types so also check a subtype
        o = ArrayList()
        with self.assertRaises(AttributeError):
            del o.add
        with self.assertRaises(AttributeError):
            o.bad = 7

    def test_java_name(self):
        self.assertEqual(Object.java_name, "java.lang.Object")
        self.assertEqual(Object().java_name, "java.lang.Object")
