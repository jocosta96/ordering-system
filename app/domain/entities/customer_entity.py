class Customer:
    #dataclass
    def __init__(
            self,
            document,
            email,
            name,
            id
        ):
        
        self.document = document
        self.email = email
        self.name = name
        self.id = id

