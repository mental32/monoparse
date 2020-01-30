from operator import rshift

from monoparse import Parser, OneOrMore, Silent, Maybe, ASCII_DIGITS

# "Whitespaces" is a rule that matches one or more space characters
#
# We also mark it as silent because we don't want to capture any
# Whitespace products as they are useless to a calculator...
Whitespaces = Silent(OneOrMore(" "))

# "Number" is a rule that uses an already provided rule "ASCII_DIGITS"
#
# Here we simply describe what we consider a number to be.
# "ASCII_DIGITS" is equivelent to ``OneOrMore(ASCII_DIGIT)``
# Where "ASCII_DIGIT" is ``OneOf(string.digits)``.
Number = Maybe("-") >> ASCII_DIGITS

# An "Operator" is matched against any one of "+", "-", "*" or "/"
#
# It's synonymous to: ``(Atom("+") | "-" | "*" | "/")``
Operator = OneOf("+-*/")

# "Base" is our starting rule.
Base = (
    Number
    >> Whitespaces
    >> Maybe(OneOrMore(Operator >> Whitespaces >> Number))
)

ast: List[Union[Number, Operator]]

# For now: any two argument operator can be used as a joining operator, we must specify explicitly.
ast = Base.parse("89 * 3 / -735", joined_by=rshift)
