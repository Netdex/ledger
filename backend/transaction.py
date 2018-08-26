schema = {
    "$id": "http://example.com/example.json",
    "type": "object",
    "additionalProperties": False,
    "definitions": {
        "account_list": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "account": {
                        "type": "string",
                        "minLength": 1
                    },
                    "amount": {
                        "type": "integer",
                        "minimum": 1
                    }
                },
                "required": [
                    "account",
                    "amount"
                ]
            }
        }
    },
    "properties": {
        "id": {
            "type": "string"
        },
        "date": {
            "type": "string",
            "pattern": "^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$"
        },
        "reason": {
            "type": "string",
            "minLength": 1
        },
        "src": {"$ref": "#/definitions/account_list"},
        "dest": {"$ref": "#/definitions/account_list"},

    },
    "required": [
        "date",
        "reason",
        "src",
        "dest"
    ]
}
