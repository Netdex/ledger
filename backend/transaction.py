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
                        "type": "number",
                        "minimum": 0.01
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
        "datetime": {
            "type": "string",
            "format": "date-time"
        },
        "reason": {
            "type": "string",
            "minLength": 1
        },
        "transactions": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "src": {"$ref": "#/definitions/account_list"},
                    "dest": {"$ref": "#/definitions/account_list"}
                },
                "required": [
                    "src",
                    "dest"
                ]
            }
        }
    },
    "required": [
        "reason",
        "transactions"
    ]
}
