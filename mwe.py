from talon.signature.bruteforce import extract_signature

message = """Wow. Awesome!
--
Bob Smith

If you do not wish to receive further emails from us, click here to unsubscribe."""

text, signature = extract_signature(message)

print('Signature found: \n' + str(signature) + '\n')

# Question posted to https://stackoverflow.com/questions/55815892/mailgun-talon-matches-very-few-email-signatures
'''
talon works only in very specific contexts, with clean signatures and very little "noise" around them.

Although it works with the examples given in the docs, it fails to find any sigs in the many test emails I've fed it. For example, if there are more than 61 characters after the sig, it fails to match anything.

```python
from talon.signature.bruteforce import extract_signature

message = """Wow. Awesome!
--
Bob Smith

If you do not wish to receive further emails from us, click here to unsubscribe."""

text, signature = extract_signature(message)

print('Signature found:\n' + str(signature) + '\n')
```

This returns `Signature found:\n None`, rather than the expected `Signature found:\n--\nBob Smith`. However, if the line after the sig is reduced to <62 characters (stopping after the word `click`), it returns the sig plus the extra line, which it shouldn't.

The ML version of talon fails similarly with the same input (can provide an MWE.

The docs say that the heuristic version will work for 90% of the cases, and the ML version should cover the remaining 10%, which makes me think I'm missing something, as the heuristic and ML versions combined are catching a negligible proportion of the emails I've fed it. Any ideas what might be going wrong? Thanks.
'''
