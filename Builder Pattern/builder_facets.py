class Person:
    def __init__(self):
        print('Creating an instance of Person')
        # Address-related info
        self.street_address = None
        self.postcode = None
        self.city = None
        # Job-related info
        self.company_name = None
        self.position = None
        self.annual_income = None

    def __str__(self) -> str:
        return (
            f'Address: {self.street_address}, {self.postcode}, {self.city}\n'
            f'Employed at {self.company_name} as a {self.position} earning {self.annual_income}'
        )


# ---------------------------
# FACADE BUILDER (main entry)
# ---------------------------
class PersonBuilder:
    """
    Acts as a single entry point (facade) for building Person objects.
    Delegates to specialized builders for address and job details.
    """

    def __init__(self, person=None):
        # If no person passed in, create a new one
        if person is None:
            self.person = Person()
        else:
            self.person = person

    @property
    def lives(self):
        # Switch to the "Address builder"
        return PersonAddressBuilder(self.person)

    @property
    def works(self):
        # Switch to the "Job builder"
        return PersonJobBuilder(self.person)

    def build(self):
        # Return the fully constructed Person
        return self.person


# ---------------------------
# JOB BUILDER
# ---------------------------
class PersonJobBuilder(PersonBuilder):
    """
    Builder specialized for setting job-related details.
    """

    def __init__(self, person):
        super().__init__(person)

    def at(self, company_name):
        self.person.company_name = company_name
        return self  # fluent API

    def as_a(self, position):
        self.person.position = position
        return self

    def earning(self, annual_income):
        self.person.annual_income = annual_income
        return self


# ---------------------------
# ADDRESS BUILDER
# ---------------------------
class PersonAddressBuilder(PersonBuilder):
    """
    Builder specialized for setting address-related details.
    """

    def __init__(self, person):
        super().__init__(person)

    def at(self, street_address):
        self.person.street_address = street_address
        return self

    def with_postcode(self, postcode):
        self.person.postcode = postcode
        return self

    def in_city(self, city):
        self.person.city = city
        return self


# ---------------------------
# USAGE
# ---------------------------
if __name__ == '__main__':
    # Build a fully-detailed person using sub-builders
    pb = PersonBuilder()
    p = (
        pb
        .lives
            .at('123 London Road')
            .in_city('London')
            .with_postcode('SW12BC')
        .works
            .at('Fabrikam')
            .as_a('Engineer')
            .earning(123000)
        .build()
    )
    print(p)

    # Build an "empty" person (no data set)
    person2 = PersonBuilder().build()
    print(person2)
