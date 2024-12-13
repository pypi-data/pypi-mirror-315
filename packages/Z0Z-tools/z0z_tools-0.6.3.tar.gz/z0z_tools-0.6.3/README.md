# Z0Z_tools

A collection of tools to solve common Python development frustrations. "Z0Z_" indicates these are prototype solutions - they work, but might not be pretty.

## Tired of handling string vs boolean parameter confusion?

Add `oopsieKwargsie()` to your function: it intelligently converts string parameters to their proper boolean or None types.

## Need flexible control over parallel processing?

Add a flexible parameter to your function, and use `defineConcurrencyLimit()` to give users more control over concurrent processing by using intuitive ratios or counts:

- Use fractions (0.75 = 75% of CPUs)
- Specify exact counts (8 = use 8 CPUs)
- Use negative values (-2 = total CPUs minus 2)

## Extract data as strings from simple or complex nested data structures?

Extract and standardize values from complex data structures with `stringItUp()`:

- Recursively unpack nested structures
- Convert all elements to strings
- Handle arbitrary iterables and custom objects

## Want to merge multiple dictionaries of lists?

`updateExtendPolishDictionaryLists()` can combine and clean dictionary data with optional:

- Duplicate removal
- List sorting
- Error handling for incompatible data

## "I just want to load the audio: I don't need 714 options!"

Load audio, `readAudioFile()`, and save WAV files, `writeWav()`, without the complexity:

- Automatic stereo conversion
- Sample rate control
- Multi-file batch processing, too: `loadWaveforms()`

## Want to create relative paths between any two locations?

Convert between paths easily with `findRelativePath()`:

- Works with files or directories
- Handles paths on different branches
- Supports both string and Path-like inputs
- Returns platform-independent paths

## Need to validate integer inputs?

`intInnit()` rigorously validates and converts input lists to integers:

- Converts valid numeric types to integers
- Rejects non-whole numbers
- Provides clear error messages
- Perfect for validating user inputs

## Want to install a package that lacks proper installation files?

If you have a Python package that doesn't have an installation file, `pipAnything()` creates a temporary setup environment to help `pip` install the unpackaged code.

```sh
python -m Z0Z_tools.pipAnything <pathPackage>
```

## Installation

```sh
pip install Z0Z-tools
```
