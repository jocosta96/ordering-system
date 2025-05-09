class Customer:
    #dataclass
    def __init__(
            self,
            document,
            email,
            name
        ):
        
        self.document = document
        self.email = email
        self.name = name
