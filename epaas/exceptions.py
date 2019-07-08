from __future__ import unicode_literals
import dataent

# accounts
class PartyFrozen(dataent.ValidationError): pass
class InvalidAccountCurrency(dataent.ValidationError): pass
class InvalidCurrency(dataent.ValidationError): pass
class PartyDisabled(dataent.ValidationError):pass
