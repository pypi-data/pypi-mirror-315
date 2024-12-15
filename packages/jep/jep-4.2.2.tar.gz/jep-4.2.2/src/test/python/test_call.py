import unittest

import jep
Test = jep.findClass('jep.test.Test')
Boolean = jep.findClass('java.lang.Boolean')
StringBuilder = jep.findClass('java.lang.StringBuilder')
ArrayList = jep.findClass('java.util.ArrayList')

class TestTypes(unittest.TestCase):

    def setUp(self):
        self.test = Test()

    def test_enum(self):
        testEnum = self.test.getEnum()
        self.assertEqual(0, testEnum.ordinal())

    def test_getstring_array(self):
        obj = self.test.getStringArray()
        self.assertEqual('one', obj[0])
        self.assertEqual('two', obj[1])
        self.assertEqual('one two', ' '.join(obj))

    def test_string_string_array(self):
        obj = self.test.getStringStringArray()
        self.assertEqual('one', obj[0][0])

    def test_int_array(self):
        obj = self.test.getIntArray()
        self.assertEqual(1, obj[0])

    def test_bool_array(self):
        obj = self.test.getBooleanArray()
        self.assertTrue(obj[1])

    def test_short_array(self):
        obj = self.test.getShortArray()
        self.assertEqual(123, obj[0])

    def test_float_array(self):
        obj = self.test.getFloatArray()
        self.assertAlmostEqual(123.12300109863281, obj[0])

    def test_object_array(self):
        obj = self.test.getObjectArray()
        self.assertEqual(self.test.toString(), obj[0].toString())

    def test_equals(self):
        self.assertTrue(self.test.getClass() == Test)
        from java.lang import Class, String, Integer
        self.assertFalse(self.test.getClass() == Class)
        self.assertEqual(String('one'), String('one'))
        self.assertTrue(String('1') == String('1'))
        self.assertEqual(self.test, self.test)
        self.assertNotEqual(self.test, Test())
        self.assertNotEqual(String('two'), String('one'))

        self.assertEqual(String, String)
        self.assertNotEqual(String, Integer)

    def test_20args(self):
        args = list()
        for x in range(20):
            args.append(Test())
        result = Test.test20Args(*args)
        self.assertEqual(args, list(result))

    def test_deepList(self):
        # Make sure type conversion works when a list contains a list...
        l = [self.test]
        for i in range(50):
            l = [l]
        result = self.test.testObjectPassThrough(l)
        for i in range(50):
            result = result[0]
        self.assertEqual(self.test, result[0])

    def test_overload(self):
        builder = StringBuilder()
        builder.append(1)
        self.assertTrue(builder.toString() == "1")
        builder = StringBuilder()
        builder.append(StringBuilder)
        self.assertTrue(builder.toString() == "class java.lang.StringBuilder")
        list = ArrayList()
        list.add("One")
        list.add("Two")
        list.add("Three")
        list.remove(1)
        self.assertEqual(list.size(), 2)

    def test_empty_kwargs(self):
        # Some frameworks will pass an empty kwargs dict when there are no kwargs.
        # pyjmethods pyjconstructors and pyjmultimethods should handle this
        l = []
        d = {}
        a = ArrayList(*l, **d)
        # In a normal call python will end up removing the empty kwargs before
        # it reaches jep objects so use __func__ to call more directly.
        a.add.__func__(a, 1, *l, **d)
        self.assertEqual(1, a.size.__func__(a, *l, **d))

    def test_callback(self):
        expected = ArrayList([1, 2, 3, 4, 5])
        actual = ArrayList()
        expected.forEach(actual.add)
        self.assertTrue(expected == actual)

    def test_stream_callbacks(self):
        from java.util.stream import LongStream
        result = LongStream.range(1, 1000)\
            .filter(lambda i: i % 2 == 0)\
            .reduce(lambda first, second: first + second)\
            .getAsLong()
        self.assertTrue(result == sum(range(2, 1000, 2)))

    def test_observer(self):
        from java.util.concurrent import Executors
        a = list()
        def runTask():
            a.append(1)
        Executors.callable(runTask).call()
        self.assertEqual(len(a), 1)

    def test_vararg(self):
        from java.util import Arrays
        self.assertSequenceEqual((), Arrays.asList())
        self.assertSequenceEqual(("1"), Arrays.asList("1"))
        self.assertSequenceEqual(("1","2"), Arrays.asList("1","2"))
        # Passing a tuple should convert the tuple elements to the varargs array.
        self.assertSequenceEqual(("1","2"), Arrays.asList(("1","2")))
        # instance method as opposed to static method above
        self.assertSequenceEqual(("1","2"), self.test.testAllVarArgs("1","2"))
        # Multiple varargs goes through a different path then just one vararg so be sure to hit both.
        self.assertSequenceEqual(("1"), self.test.testAllVarArgs("1"))
        # Varags with a @PyMethod annotation
        self.assertSequenceEqual(("1","2"), self.test.testAllVarArgsAnnotated("1","2"))
        # mixing normal args with varargs
        self.assertSequenceEqual(("1","2", "3"), self.test.testMixedVarArgs("1","2", "3"))
        self.assertSequenceEqual(("1","2", "3", "4"), self.test.testMixedVarArgs("1","2", "3", "4"))

    def test_constructor_varargs(self):
        self.assertSequenceEqual(("1", ), Test("1").getConstructorVarArgs());
        # Non-varargs should be chosen over varargs when possible
        self.assertEqual(None, Test("1", "2").getConstructorVarArgs());
        self.assertSequenceEqual(("1", "2", "3"), Test("1", "2", "3").getConstructorVarArgs());
        # Passing a tuple should convert the tuple elements to the varargs array.
        self.assertSequenceEqual(("1", "2", "3"), Test(("1", "2", "3")).getConstructorVarArgs());

    def test_kwarg(self):
        expected = {"k1":"v1", "k2":"v2"};
        actual = self.test.testKwArgsMap(k1="v1", k2="v2")
        self.assertEqual(expected, dict(actual))
        actual = self.test.testKwArgsMap(**expected)
        self.assertEqual(expected, dict(actual))
        actual = self.test.testKwArgsDict(k1="v1", k2="v2")
        self.assertEqual(expected, actual)
        actual = self.test.testKwArgsDict(**expected)
        self.assertEqual(expected, actual)

        actual = self.test.testKwArgsMap()
        self.assertEqual(None, actual)
        actual = self.test.testKwArgsDict()
        self.assertEqual(None, actual)

        varargs = ("1", "2")
        result = self.test.testVarAndKwArgsMap(*varargs, **expected)
        self.assertSequenceEqual(varargs, result[:2])
        self.assertEqual(expected, dict(result[2]))

        varargs = ("1", "2")
        result = self.test.testMixedVarAndKwArgsMap("0", *varargs, **expected)
        self.assertEqual("0", result[0])
        self.assertSequenceEqual(varargs, result[1:3])
        self.assertEqual(expected, dict(result[3]))

        # When no kwargs are provided a method without kwargs should take precedence over a method with kwargs
        self.assertEqual("No Args", self.test.testKwArgsOverloaded())
        # But when kwargs are provided the kwargs method should be chosen
        self.assertEqual(expected, self.test.testKwArgsOverloaded(**expected))


