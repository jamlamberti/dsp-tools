# DSP-Tools

[![Build Status](https://travis-ci.com/jamlamberti/dsp-tools.svg?branch=master)](https://travis-ci.com/jamlamberti/dsp-tools) [![Coverage Status](https://coveralls.io/repos/github/jamlamberti/dsp-tools/badge.svg?branch=master)](https://coveralls.io/github/jamlamberti/dsp-tools?branch=master) [![codecov](https://codecov.io/gh/jamlamberti/dsp-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/jamlamberti/dsp-tools) [![Maintainability](https://api.codeclimate.com/v1/badges/1a3e9f43b31549d2aefb/maintainability)](https://codeclimate.com/github/jamlamberti/dsp-tools/maintainability)


A framework for prototyping DSP systems. Includes a collection of sources and
blocks which allow for operations on the sources. The framework will fetch data
from a source when necessary as opposed to having a big queue. Part of the
reason for this is that the system is designed to operate over an unbounded
horizon.


Take the following example:


```python
from signal_generators.basic_signals import StepNumber

step_number = StepNumber()

# THIS WILL INFINITE LOOP
for step in step_number():
    print step
```


While this may seem undesirable, virtually all real DSP systems are running
over an unbounded horizon. This allows for taking any code developed with the
framework and using it in a more realistic environment, where sources and sinks
are interacting with external systems.


However, preventing infinite loops is easy! DSP-Tools supports a few signal
types such as Finite Length Signals. Because of the lazy data fetch, the output
signals from a system can just be wrapped into a FiniteLengthSignal as shown
below.


```python
from signal_generators.basic_signals import StepNumber
from signal_generators.signal_types import FiniteLengthSignal


NUM_STEPS = 10


step_number = StepNumber()
step_number_finite = FiniteLengthSignal(NUM_STEPS, step_number)

for step in step_number_finite():
    print step
```
