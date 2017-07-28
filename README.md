# DesignPy

This tool provides feedback on the design and style of Python code, specifically on:

- formatting of comments
- amount of commenting
- consistency of indentation type
- line length violations
- length of identifiers
- use of whitespace around operators

## Installation

	pip install designpy

## Usage

	designpy <filename>

## Example

	# designpy getaltheorie.py
	
	:) blank lines before all comments
	:( consistent indentation
	  -?inconsistent indentation at: for priems2 in range(len(list_priem)):
	:( all lines contain max 80 characters
	:S possibly too short names: ['p']
	:) exclusively using tabs or spaces for indentation
	:( missing whitespace around operator
	  -p=3
	:) blank lines before all comments
	:( consistent indentation
	  -?inconsistent indentation at: for priems2 in range(len(list_priem)):
	:( all lines contain max 80 characters
	:S possibly too short names: ['p']
	:) exclusively using tabs or spaces for indentation
	:( missing whitespace around operator
	  -p=3

As you can see, `designpy` provides positive as well as negative feedback, sometimes with examples. In a couple of cases, the tool can provide "unsure" feedback about suspicious style.

## Contributing

Feel free to submit pull requests through GitHub. All contributions must be made available under the MIT license.
