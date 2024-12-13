from typing import Optional, Union, Callable, Any
import pytest
from unittest.mock import patch
from Z0Z_tools import defineConcurrencyLimit, oopsieKwargsie

@pytest.fixture
def mockCpuCount():
    """Fixture to mock multiprocessing.cpu_count(). Always returns 8."""
    with patch('multiprocessing.cpu_count', return_value=8):
        yield

@pytest.mark.parametrize("variantTrue", ['True', 'TRUE', ' true ', 'TrUe'])
def testOopsieKwargsieHandlesTrueVariants(variantTrue):
    """Test oopsieKwargsie handles various string representations of True."""
    assert oopsieKwargsie(variantTrue) is True

@pytest.mark.parametrize("variantFalse", ['False', 'FALSE', ' false ', 'FaLsE'])
def testOopsieKwargsieHandlesFalseVariants(variantFalse):
    """Test oopsieKwargsie handles various string representations of False."""
    assert oopsieKwargsie(variantFalse) is False

@pytest.mark.parametrize("variantNone", ['None', 'NONE', ' none ', 'NoNe'])
def testOopsieKwargsieHandlesNoneVariants(variantNone):
    """Test oopsieKwargsie handles various string representations of None."""
    assert oopsieKwargsie(variantNone) is None

@pytest.mark.parametrize("stringInput", ['hello', '123', 'True story', 'False alarm'])
def testOopsieKwargsieReturnsOriginalString(stringInput):
    """Test oopsieKwargsie returns the original string when input is unrecognized."""
    assert oopsieKwargsie(stringInput) == stringInput

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (None, 8),
    (False, 8),
    (0, 8),
])
def testDefineConcurrencyLimitDefaults(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with default parameters."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (1, 1),
    (4, 4),
    (16, 16),
])
def testDefineConcurrencyLimitDirectIntegers(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with direct integer values ≥ 1."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (0.5, 4),
    (0.25, 2),
    (0.75, 6),
])
def testDefineConcurrencyLimitFractionalFloats(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with float values between 0 and 1."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (-0.5, 4),
    (-0.25, 6),
    (-0.75, 2),
])
def testDefineConcurrencyLimitNegativeFractions(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with float values between -1 and 0."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (-1, 7),
    (-3, 5),
    (-7, 1),
])
def testDefineConcurrencyLimitNegativeIntegers(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with integer values ≤ -1."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
def testDefineConcurrencyLimitBooleanTrue():
    """Test defineConcurrencyLimit with boolean True."""
    resultLimit = defineConcurrencyLimit(True)
    assert resultLimit == 1

@pytest.mark.usefixtures("mockCpuCount")
def testDefineConcurrencyLimitSpecificTrueCase():
    """Ensure defineConcurrencyLimit(True) specifically returns 1."""
    resultTrue = defineConcurrencyLimit(True)
    resultNone = defineConcurrencyLimit(None)
    assert resultTrue == 1
    assert resultNone != 1

@pytest.mark.usefixtures("mockCpuCount")
@patch('Z0Z_tools.parseParameters.oopsieKwargsie')
@pytest.mark.parametrize("stringInput, mockedReturn, expectedLimit", [
    ("true", True, 1),
    ("false", False, 8),
    ("none", None, 8),
    ("4", 4, 4),
])
def testDefineConcurrencyLimitStringValues(mockOopsieKwargsie, stringInput, mockedReturn, expectedLimit):
    """Test defineConcurrencyLimit handling of string inputs via oopsieKwargsie."""
    mockOopsieKwargsie.return_value = mockedReturn
    resultLimit = defineConcurrencyLimit(stringInput)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (-10, 1),
    (-0.99, 1),
    (0.1, 1),
])
def testDefineConcurrencyLimitEnsuresMinimumOne(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit ensures the minimum return value is 1."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

def makeTestSuiteOopsieKwargsie(functionUnderTest: Callable[[str], Optional[Union[bool, str]]]):
    """
    Creates a test suite for oopsieKwargsie-like functions.
    
    Parameters:
        functionUnderTest: The function to test, must accept str and return bool|None|str

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    def testHandlesTrueVariants():
        for variantTrue in ['True', 'TRUE', ' true ', 'TrUe']:
            assert functionUnderTest(variantTrue) is True

    def testHandlesFalseVariants():
        for variantFalse in ['False', 'FALSE', ' false ', 'FaLsE']:
            assert functionUnderTest(variantFalse) is False

    def testHandlesNoneVariants():
        for variantNone in ['None', 'NONE', ' none ', 'NoNe']:
            assert functionUnderTest(variantNone) is None

    def testReturnsOriginalString():
        for stringInput in ['hello', '123', 'True story', 'False alarm']:
            assert functionUnderTest(stringInput) == stringInput

    return {
        'testHandlesTrueVariants': testHandlesTrueVariants,
        'testHandlesFalseVariants': testHandlesFalseVariants,
        'testHandlesNoneVariants': testHandlesNoneVariants,
        'testReturnsOriginalString': testReturnsOriginalString
    }

def makeTestSuiteConcurrencyLimit(functionUnderTest: Callable[[Any], int], cpuCount: int = 8):
    """
    Creates a test suite for defineConcurrencyLimit-like functions.
    
    Parameters:
        functionUnderTest: The function to test, must return int
        cpuCount (8): Number of CPUs to simulate

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testDefaults(_mockCpu):
        for limitParameter in [None, False, 0]:
            assert functionUnderTest(limitParameter) == cpuCount

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testDirectIntegers(_mockCpu):
        for limitParameter in [1, 4, 16]:
            assert functionUnderTest(limitParameter) == limitParameter

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testFractionalFloats(_mockCpu):
        testCases = {
            0.5: cpuCount // 2,
            0.25: cpuCount // 4,
            0.75: int(cpuCount * 0.75)
        }
        for input, expected in testCases.items():
            assert functionUnderTest(input) == expected

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testMinimumOne(_mockCpu):
        for limitParameter in [-10, -0.99, 0.1]:
            assert functionUnderTest(limitParameter) >= 1

    return {
        'testDefaults': testDefaults,
        'testDirectIntegers': testDirectIntegers,
        'testFractionalFloats': testFractionalFloats,
        'testMinimumOne': testMinimumOne
    }

def makeTestSuiteIntInnit(functionUnderTest):
    """
    Creates a test suite for intInnit-like functions.
    
    Parameters:
        functionUnderTest: The function to test, must accept list and return list[int]

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    def testHandlesValidIntegers():
        assert functionUnderTest([1, 2, 3], 'test') == [1, 2, 3]
        assert functionUnderTest([1.0, 2.0, 3.0], 'test') == [1, 2, 3]

    def testRejectsNonWholeNumbers():
        with pytest.raises(ValueError):
            functionUnderTest([1.5, 2, 3], 'test')

    def testRejectsBooleans():
        with pytest.raises(TypeError):
            functionUnderTest([True, False], 'test')

    def testRejectsNonNumerics():
        with pytest.raises(TypeError):
            functionUnderTest(['1', '2', '3'], 'test')

    def testRejectsEmptyList():
        with pytest.raises(ValueError):
            functionUnderTest([], 'test')

    def testHandlesMixedValidTypes():
        assert functionUnderTest([1, 2.0, 3], 'test') == [1, 2, 3]

    return {
        'testHandlesValidIntegers': testHandlesValidIntegers,
        'testRejectsNonWholeNumbers': testRejectsNonWholeNumbers,
        'testRejectsBooleans': testRejectsBooleans,
        'testRejectsNonNumerics': testRejectsNonNumerics,
        'testRejectsEmptyList': testRejectsEmptyList,
        'testHandlesMixedValidTypes': testHandlesMixedValidTypes
    }

@pytest.mark.parametrize("input_list,expected", [
    ([1, 2, 3], [1, 2, 3]),
    ([1.0, 2.0, 3.0], [1, 2, 3]),
    ([1, 2.0, 3], [1, 2, 3]),
])
def testIntInnitValidCases(input_list, expected):
    """Test intInnit with valid inputs."""
    from Z0Z_tools import intInnit
    assert intInnit(input_list, 'test') == expected

@pytest.mark.parametrize("invalid_input,expected_error", [
    ([1.5, 2, 3], ValueError),
    ([True, False], TypeError),
    (['1', '2', '3'], TypeError),
    ([], ValueError),
])
def testIntInnitInvalidCases(invalid_input, expected_error):
    """Test intInnit with invalid inputs."""
    from Z0Z_tools import intInnit
    with pytest.raises(expected_error):
        intInnit(invalid_input, 'test')