from jsonschema import validate
import jsonschema

json = {

    "tall": False,
    "short": False 

}
schema = {
    "type": "object",
    "properties":{
        "tall": {"type": "boolean"},
        "short": {"type": "boolean"}
    },
    "not":{
        "allOf":[
            { "properties": { "tall": {"const": True}  } },
            { "properties": {"short": {"const": True} } }
        ]
    }
}

try:
    validate(schema = schema, instance= json)
    print("Working fine")
except jsonschema.exceptions.ValidationError as err:
    print(err)

