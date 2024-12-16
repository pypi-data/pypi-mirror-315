import sys
from typing import List
from enum import Enum

_orig_module = sys.modules[__name__]

class TokenType(Enum):
	NUMBER = 'NUMBER'
	OPERATOR = 'OPERATOR'
	DOT = 'DOT'
	VARIABLE = 'VARIABLE'
	PAREN = 'PAREN'

class Token:
	def __init__(self, token_type: TokenType, value: str):
		self.token_type = token_type
		self.value = value

	def __str__(self):
		return f"Token<{self.token_type}>({self.value})"

# https://stackoverflow.com/a/493788/4454877
def _text2int(textnum: str, numwords={}) -> int | None:
	if not numwords:
		units = [
			"zero", "one", "two", "three", "four", "five", "six", "seven",
			"eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
			"fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
		]
		tens = [
			"", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
			"eighty", "ninety",
		]
		scales = [
			"hundred", "thousand", "million", "billion", "trillion", "quadrillion",
			"quintillion", "sextillion", "septillion", "octillion", "nonillion",
			"decillion", "undecillion", "duodecillion", "tredecillion",
			"quattuordecillion", "quindecillion", "sexdecillion", "septemdecillion",
			"octodecillion", "novemdecillion", "vigintillion", "unvigintillion",
			"duovigintillion", "tresvigintillion", "quattuorvigintillion", "quinvigintillion",
			"sesvigintillion", "septemvigintillion", "octovigintillion", "novemvigintillion",
			"trigintillion", "untrigintillion", "duotrigintillion", "trestrigintillion",
			"quattuortrigintillion", "quintrigintillion", "sestrigintillion", "septentrigintillion",
			"octotrigintillion", "noventrigintillion", "quadragintillion", "unquadragintillion",
			"duoquadragintillion", "tresquadragintillion", "quattuorquadragintillion", "quinquadragintillion",
			"sesquadragintillion", "septenquadragintillion", "octoquadragintillion", "novenquadragintillion",
			"quinquagintillion", "unquinquagintillion", "duoquinquagintillion", "trequinquagintillion",
			"quattuorquinquagintillion", "quinquinquagintillion", "sesquinquagintillion", "septenquinquagintillion",
			"octoquinquagintillion", "novenquinquagintillion", "sexagintillion", "unsexagintillion", "duosexagintillion",
			"tresexagintillion", "quattuorsexagintillion", "quinsexagintillion", "sesexagintillion", "septensexagintillion",
			"octosexagintillion", "novensexagintillion", "septuagintillion", "unseptuagintillion", "duoseptuagintillion",
			"treseptuagintillion", "quattuorseptuagintillion", "quinseptuagintillion", "seseptuagintillion",
			"septenseptuagintillion", "octoseptuagintillion", "novenseptuagintillion", "octogintillion", "unoctogintillion",
			"duooctogintillion", "tresoctogintillion", "quattuoroctogintillion", "quinoctogintillion", "sexoctogintillion",
			"septemoctogintillion", "octooctogintillion", "novemoctogintillion", "nonagintillion", "unnonagintillion", 
			"duononagintillion", "trenonagintillion", "quattuornonagintillion", "quinnonagintillion", "senonagintillion", 
			"septenonagintillion", "octononagintillion", "novenonagintillion", "centillion", # PRs welcome (seriously)
		]
		numwords["and"] = (1, 0)
		for idx, word in enumerate(units):  numwords[word] = (1, idx)
		for idx, word in enumerate(tens):   numwords[word] = (1, idx * 10)
		for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

	current = result = 0
	for word in textnum.split():
		if word not in numwords:
			return None
		scale, increment = numwords[word]
		current = current * scale + increment
		if scale > 100:
			result += current
			current = 0

	return result + current

def _get_caller_scope():
	"""Get the locals and globals from the caller's frame"""
	# Get caller's frame (3 levels up: beyond getattr and this function)
	frame = sys._getframe(3)
	return frame.f_locals, frame.f_globals

def _tokenize(name: str) -> List[Token]:
    """Convert a name like TWO_HUNDRED_PLUS_X into tokens"""
    tokens = []
    locals_dict, globals_dict = _get_caller_scope()
    parts = name.split('_')
    i = 0
    while i < len(parts):
        part = parts[i]
        
        # Handle operators
        if part in ['PLUS', 'MINUS', 'TIMES', 'DIVIDED', 'BY']:
            if part == 'DIVIDED':
                if i + 1 < len(parts) and parts[i + 1] == 'BY':
                    tokens.append(Token(TokenType.OPERATOR, '/'))
                    i += 2
                    continue
                else:
                    raise ValueError("DIVIDED must be followed by BY")
            elif part == 'BY':
                raise ValueError("Unexpected BY without DIVIDED")
            else:
                op_map = {'PLUS': '+', 'MINUS': '-', 'TIMES': '*'}
                tokens.append(Token(TokenType.OPERATOR, op_map[part]))
            i += 1
            continue
        
        # Handle POINT/DOT
        if part in ['POINT', 'DOT']:
            tokens.append(Token(TokenType.DOT, '.'))
            i += 1
            continue

        # Handle parentheses
        if part == 'OPEN':
            tokens.append(Token(TokenType.PAREN, '('))
            i += 1
            continue
        elif part == 'CLOSE':
            tokens.append(Token(TokenType.PAREN, ')'))
            i += 1
            continue
        
        # Check for variables first (single token)
        if (part[0].isupper() and 
            all(c.isupper() or c.isdigit() for c in part) and 
            (part in locals_dict or part in globals_dict)):
            tokens.append(Token(TokenType.VARIABLE, part))
            i += 1
            continue
        
        # Try to parse number - look ahead to build complete number phrase
        num_phrase = []
        j = i
        while j < len(parts):
            next_part = parts[j]
            # Stop if we hit an operator, special token, or potential variable
            if (next_part in ['PLUS', 'MINUS', 'TIMES', 'DIVIDED', 'BY', 'POINT', 'DOT', 'OPEN', 'CLOSE'] or
                (next_part[0].isupper() and 
                 all(c.isupper() or c.isdigit() for c in next_part) and 
                 (next_part in locals_dict or next_part in globals_dict))):
                break
            num_phrase.append(next_part.lower())
            j += 1
            
        if num_phrase:  # Try to parse the complete phrase
            num_value = _text2int(' '.join(num_phrase))
            if num_value is not None:
                tokens.append(Token(TokenType.NUMBER, str(num_value)))
                i = j  # Skip past all parts we used
                continue
        
        # If we get here, it wasn't a valid number, variable, or any other valid token
        raise ValueError(f"Invalid token: {part}")
    
    return tokens

def _evaluate(tokens: List[Token]) -> float:
    """Evaluate a list of tokens respecting operator precedence and parentheses"""
    # First, resolve variables
    locals_dict, globals_dict = _get_caller_scope()
    resolved_tokens = []

    for token in tokens:
        if token.token_type == TokenType.VARIABLE:
            # Look up variable in caller's scope
            var_name = token.value
            if var_name in locals_dict:
                value = locals_dict[var_name]
            elif var_name in globals_dict:
                value = globals_dict[var_name]
            else:
                raise ValueError(f"Variable {var_name} not found in scope")
            resolved_tokens.append(Token(TokenType.NUMBER, str(float(value))))
        else:
            resolved_tokens.append(token)

    # First pass: combine numbers with dots
    combined_tokens = []
    i = 0
    while i < len(resolved_tokens):
        if (i + 2 < len(resolved_tokens) and
            resolved_tokens[i].token_type == TokenType.NUMBER and
            resolved_tokens[i + 1].token_type == TokenType.DOT and
            resolved_tokens[i + 2].token_type == TokenType.NUMBER):
            # Combine the float
            value = f"{resolved_tokens[i].value}.{resolved_tokens[i + 2].value}"
            combined_tokens.append(Token(TokenType.NUMBER, value))
            i += 3
        else:
            combined_tokens.append(resolved_tokens[i])
            i += 1

    # Convert to postfix notation
    output = []
    operators = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}

    for token in combined_tokens:
        if token.token_type == TokenType.NUMBER:
            output.append(token)
        elif token.token_type == TokenType.PAREN:
            if token.value == '(':
                operators.append(token)
            else:  # ')'
                while operators and operators[-1].value != '(':
                    output.append(operators.pop())
                if operators:  # Remove the opening parenthesis
                    operators.pop()
                else:
                    raise ValueError("Mismatched parentheses")
        elif token.token_type == TokenType.OPERATOR:
            while (operators and 
                   operators[-1].token_type == TokenType.OPERATOR and
                   operators[-1].value != '(' and
                   precedence[operators[-1].value] >= precedence[token.value]):
                output.append(operators.pop())
            operators.append(token)
    
    while operators:
        if operators[-1].value == '(':
            raise ValueError("Mismatched parentheses")
        output.append(operators.pop())

    # Evaluate postfix expression
    stack = []
    for token in output:
        if token.token_type == TokenType.NUMBER:
            stack.append(float(token.value))
        elif token.token_type == TokenType.OPERATOR:
            if len(stack) < 2:
                raise ValueError("Invalid expression")
            b = stack.pop()
            a = stack.pop()
            if token.value == '+':
                stack.append(a + b)
            elif token.value == '-':
                stack.append(a - b)
            elif token.value == '*':
                stack.append(a * b)
            elif token.value == '/':
                if b == 0:
                    raise ValueError("Division by zero")
                stack.append(a / b)

    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack[0]

def __getattr__(name: str) -> float:
	try:
		tokens = _tokenize(name)
		val = _evaluate(tokens)
		if val is None:
			return object.__getattribute__(_orig_module, name)
		else:
			return val
	except (ValueError, IndexError) as e:
		raise AttributeError(f"Invalid expression: {name}") from e